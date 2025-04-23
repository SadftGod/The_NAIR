from functools import wraps
from modules.server_exceptions import RubberException


def not_empty(*field_names):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = args[1]  

            for field in field_names:
                if not hasattr(request, field):
                    raise RubberException.fastRubber(f"Missing field: {field}", 3)

                value = getattr(request, field)

                if isinstance(value, str):
                    value = value.strip()

                if not value:
                    raise RubberException.fastRubber(f"Field '{field}' cannot be empty", 3)

            return await func(*args, **kwargs)
        return wrapper
    return decorator