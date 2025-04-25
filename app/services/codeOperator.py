import random


class CodeOperator:
    @staticmethod
    def generate(len_of_numbers):
        if len_of_numbers < 1:
            raise ValueError("The len might be greater than 1")
        
        lower_bound = 10**(len_of_numbers - 1)
        upper_bound = (10**len_of_numbers) - 1
        return random.randint(lower_bound, upper_bound)
