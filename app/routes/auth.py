from app.proto.user import authRouter_pb2_grpc, authRouter_pb2
from app.proto.common import token_pb2
from modules.decorators.request import not_empty
from modules.decorators.exceptions import RubberCatcher
from modules.palette import Palette as p

from app.validators.userValidator import UserValidator as uv
from modules.server_exceptions import RubberException
from app.controllers.authController import AuthController as ac

class AuthRouter(authRouter_pb2_grpc.AuthServiceServicer):
    @RubberCatcher(True)
    @not_empty("login","password")
    async def Login(self, request, context):
        login,password = request.login ,request.password
        try:
            uv(login=login,password=password) \
                .password_check()\
                .nick_or_email()\
                .raise_if_invalid()
        except Exception:
            RubberException.fastRubber("Wrong login or password",3)

        token = await ac.login(login,password)

        return token_pb2.JustTokenResponse(token=token)