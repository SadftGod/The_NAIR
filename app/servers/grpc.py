import asyncio
from concurrent import futures
from grpc import aio
from app.services.routeRegistator import Route_Registrator


class GRPC_server:
   def __init__(self,max_workers:int=10):
      thread_pool = futures.ThreadPoolExecutor(max_workers=max_workers)
      server = aio.server(migration_thread_pool=thread_pool)


      rr = Route_Registrator(server if server else None)
      self.server = rr.register_all()
      
   def __call__(self):
      return self.server

