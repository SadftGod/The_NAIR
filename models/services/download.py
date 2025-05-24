from modules.palette import Palette as p
from huggingface_hub import snapshot_download, hf_hub_download, list_repo_files
from transformers import GenerationConfig, LlamaTokenizerFast
import os

class LlamaDownloader:

    REQUIRED_FILES = ["tokenizer.model", "tokenizer_config.json"]
    FALLBACK_REPOS = [
        "huggyllama/llama-7b",
        "decapoda-research/llama-7b-hf"
    ]

    def __init__(self,
                 model_name: str,
                 auth: str = None,
                 save_dir: str = "models/core/llama-7b",
                 generation_kwargs: dict = None):
        self.auth = auth
        if "/" not in model_name:
            model_name = f"decapoda-research/{model_name}"
        self.repo_id = model_name
        self.save_dir = save_dir
        self.generation_kwargs = generation_kwargs or {
            "max_new_tokens": 256,
            "do_sample": True,
            "temperature": 0.7
        }

    def download(self):
        p.yellowTag("⏬ Llama Downloader ⏬", f"Starting download '{self.repo_id}' → {self.save_dir}")
        os.makedirs(self.save_dir, exist_ok=True)

        config_path = os.path.join(self.save_dir, "config.json")
        if not os.path.isfile(config_path):
            try:
                snapshot_download(
                    repo_id=self.repo_id,
                    local_dir=self.save_dir,
                    token=self.auth
                )
                p.greenTag("✅ Llama Downloader ✅", f"Snapshot '{self.repo_id}' downloaded")
            except Exception as e:
                p.redTag("❌ Llama Downloader ❌", f"snapshot_download error: {e}")
                raise

            try:
                gen_conf = GenerationConfig(**self.generation_kwargs)
                gen_conf.save_pretrained(self.save_dir)
                p.greenTag("✅ Llama Downloader ✅", "generation_config.json created")
            except Exception as e:
                p.redTag("❌ Llama Downloader ❌", f"generation_config write error: {e}")
                raise
        else:
            p.cyanTag("ℹ️ Llama Downloader ℹ️", "Snapshot already exists, skipping download")

        missing = [
            f for f in self.REQUIRED_FILES
            if not os.path.exists(os.path.join(self.save_dir, f))
        ]
        if not missing:
            p.cyanTag("ℹ️ Llama Downloader ℹ️", "SentencePiece tokenizer already present")
        else:
            p.blueTag("💾 Llama Downloader 💾", f"Missing files: {missing}, attempting download...")
            self._download_tokenizer_files(self.repo_id, missing)

            remaining = [
                f for f in self.REQUIRED_FILES
                if not os.path.exists(os.path.join(self.save_dir, f))
            ]
            if remaining:
                p.yellowTag("⚠️ Llama Downloader ⚠️",
                           f"Files {remaining} not found in {self.repo_id}, trying fallbacks")
                for fallback in self.FALLBACK_REPOS:
                    self._download_tokenizer_files(fallback, remaining)
                    remaining = [
                        f for f in self.REQUIRED_FILES
                        if not os.path.exists(os.path.join(self.save_dir, f))
                    ]
                    if not remaining:
                        break

            still_missing = [
                f for f in self.REQUIRED_FILES
                if not os.path.exists(os.path.join(self.save_dir, f))
            ]
            if still_missing:
                raise FileNotFoundError(f"Tokenizer files not found: {still_missing}")

        json_path = os.path.join(self.save_dir, "tokenizer.json")
        if not os.path.exists(json_path):
            from transformers import LlamaTokenizer
            p.blueTag("💾 Llama Downloader 💾",
                      "tokenizer.json not found — generating from SentencePiece model")
            slow_tok = LlamaTokenizer.from_pretrained(self.save_dir, legacy=False)
            slow_tok.save_pretrained(self.save_dir)
            p.greenTag("✅ Llama Downloader ✅",
                       "tokenizer.json generated via slow tokenizer")

        tok_fast = LlamaTokenizerFast.from_pretrained(self.save_dir, legacy=False)
        p.greenTag("✅ Llama Downloader ✅", f"Fast SentencePiece tokenizer loaded: {type(tok_fast)}")

    def _download_tokenizer_files(self, repo: str, files: list[str]):
        
        try:
            available = set(list_repo_files(repo_id=repo, token=self.auth))
        except Exception as e:
            p.yellowTag("⚠️ Llama Downloader ⚠️", f"Could not list files in {repo}: {e}")
            available = set()

        for fname in files:
            if fname not in available:
                p.yellowTag("⚠️ Llama Downloader ⚠️",
                           f"{fname} not present in {repo}, skipping")
                continue
            try:
                hf_hub_download(
                    repo_id=repo,
                    filename=fname,
                    local_dir=self.save_dir,
                    token=self.auth
                )
                p.greenTag("✅ Llama Downloader ✅",
                           f"{fname} from {repo} → {self.save_dir}")
            except Exception as e:
                p.redTag("❌ Llama Downloader ❌",
                           f"Error downloading {fname} from {repo}: {e}")
