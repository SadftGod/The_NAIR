from argon2 import PasswordHasher, exceptions

class PasswordOperator:
    def __init__(self,password:str):
        self.password = password
        self.ph = PasswordHasher(
                    time_cost=3,       
                    memory_cost=65536, 
                    parallelism=4,     
                    hash_len=32,
                )

    def encode(self) -> str:
        return self.ph.hash(self.password)
    
    def compare_with(self,hash_to_compare:str)-> bool:
        try:
            return self.ph.verify(hash_to_compare, self.password)
        except exceptions.VerifyMismatchError:
            return False
