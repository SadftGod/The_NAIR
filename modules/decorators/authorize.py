from app.proto.common import token_pb2, common_pb2
from functools import wraps
from modules.server_exceptions import RubberException
from modules.palette import Palette as p
from app.services.tokenOperator import TokenOperator

def authorize():
    def decorator(func):
        @wraps(func)
        async def wrapper(self, request, context, *args, **kwargs):
            metadata = dict(context.invocation_metadata())
            auth_header = metadata.get('authorization')

            if not auth_header:
                p.redTag("Authorization error", "Missing Authorization header")
                raise RubberException("Missing Authorization header",7)
            
            if not auth_header.startswith('Bearer '):
                p.redTag("Authorization error", "Invalid Authorization header format")
                raise RubberException("Invalid Authorization header format",7)
            
            token = auth_header.split('Bearer ')[1]
            
            if not token:
                p.redTag("Authorization error", "Empty Bearer token")
                raise RubberException("Empty Bearer token",7)

            try:
                data = TokenOperator().decode_jwt(token)
                data = data.get("data")
            except Exception as e:
                RubberException.fastRubber(f"Can not decode this token: {e}",7)

            if not data:
                RubberException.fastRubber("Can not decode this token",7)

            return await func(self, request, context,data, *args, **kwargs)

        return wrapper
    return decorator
