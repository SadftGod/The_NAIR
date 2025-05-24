import re
from sentence_transformers import SentenceTransformer
from models.services.executer import Executer
from modules.palette import Palette as p
import faiss
from pathlib import Path
import pandas as pd

class RaG:
    def __init__(self,
                data_dir: str = "models/rag/data",
                model_dir: str = "models/core/llama-7b",
                embedder_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                top_k: int = 5,
                auth:str = None,
                similarity_threshold: float = 0.36,
                asking_model:str = 'nair'
):
        self.ask_part = self._find_model(asking_model)
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists() or not self.data_dir.is_dir():
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")
        self.documents = []
        
        self._load_documents()

        p.blue("Loading embedding model...")
        self.embedder = SentenceTransformer(embedder_name)
        dim = self.embedder.get_sentence_embedding_dimension()
        p.blue(f"Creating FAISS index (dim={dim})...")
        
        self.index = faiss.IndexHNSWFlat(dim, 32, faiss.METRIC_INNER_PRODUCT)
        self.index.hnsw.efConstruction = 200
        idx_file = self.data_dir / "rag_hnsw.index"
        if idx_file.exists():
            p.blue(f"Loading FAISS index from {idx_file} with mmap...")
            self.index = faiss.read_index(str(idx_file), faiss.IO_FLAG_MMAP)
        else:
            self._load_and_index()
        
        p.blue("Initializing LLaMA generator...")
        self.generator = Executer(save_dir=model_dir,load_in_4bit=True, offload_folder="offload", torch_dtype="auto",auth_token=auth)
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold
    
    def _load_documents(self):
        def chunk_text(text: str, max_length: int = 1000, overlap: int = 200) -> list[str]:
            chunks: list[str] = []
            paragraphs = text.split('\n')

            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue
                    
                if len(para) <= max_length:
                    chunks.append(para)
                    continue
                sentences = re.split(r'(?<=[.!?])\s+', para)
                current = ""
                for sent in sentences:
                    if len(current) + len(sent) + 1 <= max_length:
                        current = (current + " " + sent).strip()
                    else:
                        chunks.append(current)
                        if overlap > 0:
                            back = current[-overlap:]
                            current = (back + " " + sent).strip()
                        else:
                            current = sent
                if current:
                    chunks.append(current)

            return chunks




        for file in sorted(self.data_dir.iterdir()):
            suffix = file.suffix.lower()
            if suffix == ".txt":
                text = file.read_text(encoding="utf-8")
                header = f"[DOC: {file.name}]\n"
                chunks = chunk_text(text) if len(text) > 2000 else [text]
                for c in chunks:
                    self.documents.append(header + c)

            elif suffix in (".xls", ".xlsx", ".csv"):
                if suffix == ".csv":
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                required = ["id", "plan", "monthly_price_usd", "description"]
                missing = [col for col in required if col not in df.columns]
                if missing:
                    p.yellowTag("RAG", f"File {file.name} skipped, missing columns: {missing}")
                    continue
                for _, row in df.iterrows():
                    line = (
                        f"id: {row['id']}, plan: {row['plan']}, "
                        f"price: {row['monthly_price_usd']}, desc: {row['description']}"
                    )
                    self.documents.append(line)
    
    def _load_and_index(self):
        if not self.documents:
            p.yellowTag("RAG", "No documents indexed.")
            return
        p.blue(f"Embedding {len(self.documents)} documents...")
        embeddings = self.embedder.encode(self.documents, convert_to_numpy=True)
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)
        faiss.write_index(self.index, str(self.data_dir / "rag_hnsw.index"))
        p.greenTag("RAG", "FAISS index built.")
    
    def _find_model(self, model_name: str):
        allowed = {'mecha','nair'}
        if not model_name in allowed:
            raise ValueError(f"Model name must be one of {allowed}, but got '{model_name}'")
        if model_name == 'mecha':
            return "Ask Mecha: "
        elif model_name == 'nair':
            return "Ask Nair: "
        else:
            raise ValueError(f"Model name must be one of {allowed}, but got '{model_name}'")
       
    def retrieve(self, query: str) -> list[str]:
        query = f"{self.ask_part} {query}" 
        q_emb = self.embedder.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(q_emb)
        distances, ids = self.index.search(q_emb.reshape(1, -1), self.top_k)
        results = []
        for dist, idx in zip(distances[0], ids[0]):
            p.blue(f"RAG Debug: idx={idx}, score={dist:.4f}")
            if idx < len(self.documents) and dist >= self.similarity_threshold:
                results.append(self.documents[idx])
        if not results:
            p.yellowTag("RAG", "No relevant documents found for query.")

        return results
    
    def generate(self, query: str) -> str:
        ctxs = self.retrieve(query)
        print("🔍 Retrieved contexts:")
        for i, c in enumerate(ctxs):
            print(f"--- Chunk {i} ---\n{c}\n")

        system_inst = (
            "You are a helpful assistant That called Nair. Use the context below to answer the question. "
            "Use the style from the context where is the description of answer style"
            "Respond in full sentence. Be friendly and informative.And use the desciption from of answer from context. "
            "Don't be lazy"
        )
        context = "\n\n".join(ctxs)
        prompt = (
            f"{system_inst}\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}\n"
            f"Answer:"
        )

        p.blue("Generating with context...")
        answer = self.generator.generate(
            prompt,
            do_sample=True,
            temperature=0.75,
            top_p=0.8,
            num_return_sequences=4,
            repetition_penalty=1.2,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=2,
            length_penalty=1.0
            
        )
        return answer
