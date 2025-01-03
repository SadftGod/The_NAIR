from concurrent import futures
import grpc
from app.services.routeRegistator import Route_Registrator

class GRPC_server:
   def __init__(self):
      server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
      rr = Route_Registrator(server if server else None)
      self.server = rr.register_all()
      
   def __call__(self):
      return self.server

