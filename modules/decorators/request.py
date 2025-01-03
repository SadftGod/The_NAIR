from functools import wraps
from modules.server_exceptions import RubberException


def not_empty():
   def decorator(func):
      @wraps(func)
      def wrapper(*args,**kwargs):    
         if not args[1].ListFields():
            RubberException.fastRubber("request can not be empty",3)     
         return func(*args, **kwargs)
      return wrapper
   return decorator            
