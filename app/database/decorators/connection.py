from functools import wraps
from app.database.utils.baseModerator import BasePool

def connection(input_bases: list = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            pool = None
            names_pool = None
            b_pool = None 
            try:
                b_pool = BasePool(input_bases)
                pool = await b_pool()

                if pool and len(pool) > 0:
                    names_pool = list(pool.keys())
                return await func(*args, pool, **kwargs)
            except Exception as e:
                for db_name in names_pool:
                    await pool[db_name][0].rollback()
                raise e
            finally:
                await b_pool.close_connections(names_pool)
        return wrapper
    return decorator