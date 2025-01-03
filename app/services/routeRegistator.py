from app.routes.UserRoutes import UserRouter
from app.proto.user import user_pb2_grpc
class Route_Registrator:
   def __init__(self, server):
      self.server = server
        
   def register_all(self):
        user_pb2_grpc.add_UserRouterServicer_to_server(
            UserRouter(), self.server
        )
        
        return self.server
