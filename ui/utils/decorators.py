from functools import wraps
from starlette.requests import Request
from nicegui import ui

def require_token(page_func):
    @wraps(page_func)
    def wrapper(*args, **kwargs):
        request = next((arg for arg in args if isinstance(arg, Request)), None)
        request = request or kwargs.get('request')

        if not request or not isinstance(request, Request):
            raise ValueError("❌ Missing or invalid 'request' in @require_token-decorated function")

        token = request.cookies.get('the_nair_token')
        if not token:
            ui.navigate.to('/login')
            return
        return page_func(*args, **kwargs)
    return wrapper
