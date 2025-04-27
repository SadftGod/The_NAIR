import random
from modules.server_exceptions import RubberException

class CodeOperator:
    @staticmethod
    def generate(len_of_numbers):
        if len_of_numbers < 1:
            raise ValueError("The len might be greater than 1")
        
        lower_bound = 10**(len_of_numbers - 1)
        upper_bound = (10**len_of_numbers) - 1
        return random.randint(lower_bound, upper_bound)
    

class CodeValidator:
    @staticmethod
    def validate(code:int):
        if not isinstance(code,int):
            RubberException.fastRubber("WRONG CODE: check your email again",7)
        if code < 99999 or code > 999999:
            RubberException.fastRubber("WRONG CODE: check your email again",7)
