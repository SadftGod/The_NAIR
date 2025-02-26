from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class Configurator:
   def __init__(self):
      self.tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-3.3B")
      self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-3.3B")