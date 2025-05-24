
from app.proto.common import token_pb2,common_pb2
from functools import wraps
from modules.server_exceptions import RubberException
import psycopg.errors
from modules.palette import Palette as p

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
            except psycopg.errors.UniqueViolation as e:
               context = args[2] if len(args) > 2 else None
               if not context:
                    return token_pb2.JustTokenResponse(
                        error_response=common_pb2.DefaultErrorResponse(
                            error="Internal error: context not provided"
                        )
                    )
               if 'unfinished_registration_email_key' in str(e):
                    error_message = "Email is already registered"
               elif 'unfinished_registration_nickname_key' in str(e):
                    error_message = "The nickname has been taken"
               elif 'users_email_key' in str(e):
                    error_message = "User is exist"
               else:
                    error_message = "The rules were broken, oh oh oh"
               err = RubberException(error_message, 6)
               return build_userErrorResponse(err, args[2])

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
