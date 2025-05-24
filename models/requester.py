from models.services.llamaController import llamaController as lc


class Requester:
    @staticmethod
    def ask(query:str=""):
        return lc("baffo32/decapoda-research-llama-7B-hf").ask(query)