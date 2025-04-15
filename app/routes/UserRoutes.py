from app.proto.user import user_pb2,user_pb2_grpc
from modules.decorators.exceptions import RubberCatcher
from modules.decorators.request import not_empty
from app.services.templates.tokenTemplate import TokenAndUserTemplate
from modules.palette import Palette as p

class UserRouter(user_pb2_grpc.UserRouterServicer):
   
   @RubberCatcher(True)
   @not_empty()
   def Login(self, request, context):
      login,password,keepLogined = request.login,request.password,request.keepLogined
      taut = TokenAndUserTemplate("token",[])
      return taut.get_rpco() 
   
   @RubberCatcher(True)
   @not_empty()
   def Register(self,request,context):
      pass