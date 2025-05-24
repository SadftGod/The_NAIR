import os
from huggingface_hub import login
from modules.palette import Palette as p
from dotenv import load_dotenv
from models.services.download import LlamaDownloader as ld
from models.rag.rag import RaG

class llamaController:
    def __init__(self, model):
        self.auth = None
        self._auth()
        repo = model.lower()
        if "/" not in repo:
            repo = f"decapoda-research/{repo}"
        ld(repo, auth=self.auth).download()
        

    def ask(self,query:str=""):
        test_sentence = RaG(model_dir="models/core/llama-7b",auth=self.auth).generate(query)
        p.greenTag("Llama", f"{test_sentence}")
        return test_sentence
    def _auth(self):
        load_dotenv()
        token = os.getenv("hug") or os.getenv("HF_TOKEN")
        if token:
            try:
                login(token=token)
            except Exception:
                p.yellowTag("Llama Warning","Have not opportunity to login(), may be u r already authorized.")
            self.auth = token
        else:
            self.auth = None
