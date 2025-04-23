
from app.proto.common import token_pb2,common_pb2
from functools import wraps
from modules.server_exceptions import RubberException

def RubberCatcher(detail:bool = False):
   def build_userErrorResponse(e, context):
         if detail:
            RubberException.detail()

         error = RubberException.catcher(e, context)

         if isinstance(error, token_pb2.TokenAndUserData):
               return error
         rpce = token_pb2.JustTokenResponse(
               error_response=common_pb2.DefaultErrorResponse(
                  error=error
               ))
         return rpce
     
   def decorator(func):
         @wraps(func)
         async def wrapper(*args, **kwargs):
            try:
               return await func(*args, **kwargs)
            except Exception as e:               
               context = args[2] if len(args) > 2 else None
               if not context:
                  return token_pb2.JustTokenResponse(
                     error_response=common_pb2.DefaultErrorResponse(
                           error="Internal error: context not provided"
                     )
                  )
               return build_userErrorResponse(e, args[2])

         return wrapper
   return decorator

