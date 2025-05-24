from transformers import (
    LlamaTokenizer,
)
from modules.palette import Palette as p


class TokenizerWork:

    
    def __init__(self,sd,auth_token: str = None):
        self.tokenizer = None  
        self.safe_dir = sd
        self.auth = None
    def get_tokenizer(self):
        return self.tokenizer if self.tokenizer else self._load_tokenizer()
    def _load_tokenizer(self):
        sd = self.safe_dir
        
        #TODO : Fast Tokenizer
        p.yellow("🔄 Falling back to slow SentencePiece tokenizer")
        slow = LlamaTokenizer.from_pretrained(sd, legacy=False)
        return slow
