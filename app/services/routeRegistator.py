from app.routes.auth import AuthRouter
from app.proto.user import authRouter_pb2_grpc
class Route_Registrator:
   def __init__(self, server):
      self.server = server
        
   def register_all(self):
        authRouter_pb2_grpc.add_AuthServiceServicer_to_server(
            AuthRouter(), self.server
        )
        
        return self.server
