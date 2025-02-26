import sys
import threading
import time
from functools import wraps


class Animations:
   def loading_animation(final_print="Done"):
    """ Декоратор для отображения анимации 'Setting...' с возможностью финального сообщения """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            stop_loading = False
            
            def animate():
                nonlocal stop_loading
                symbols = ["⌛", "⌛S", "⌛Se", "⌛Set", "⌛Sett", "⌛Setti", "⌛Settin", "⌛Setting", "⌛Setting.", "⌛Setting..", "⌛Setting..."]
                i = 0
                while not stop_loading:
                    sys.stdout.write(f"\r{symbols[i % len(symbols)]} ") 
                    sys.stdout.flush()
                    time.sleep(0.2)
                    i += 1
                sys.stdout.write("\r" + " " * 20 + "\r")  
                sys.stdout.flush()

            loading_thread = threading.Thread(target=animate)
            loading_thread.start()

            try:
                result = func(*args, **kwargs)  
            finally:
                stop_loading = True  
                loading_thread.join()
            
            print(final_print)
            return result  

        return wrapper
    return decorator