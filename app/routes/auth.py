from app.proto.user import authRouter_pb2_grpc
from app.proto.common import token_pb2
from modules.decorators.request import not_empty
from modules.decorators.exceptions import RubberCatcher
from modules.decorators.authorize import authorize
from modules.palette import Palette as p

from app.validators.userValidator import UserValidator as uv
from app.validators.defaultValidator import DefaultValidator as dv
from app.services.codeOperator import CodeValidator as cv

from app.services.dateOperator import DateOperator as do

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
        
        login ,password = login.strip().lower() , password.strip()
        token = await ac.login(login,password)

        return token_pb2.JustTokenResponse(token=token)
    
    @RubberCatcher(True)
    @not_empty("email","nickname","password","language_id")
    async def Register(self, request, context):
        email,nickname ,password ,language_id = request.email ,request.nickname ,request.password ,request.language_id
        uv(nick=nickname,password=password,email=email)\
            .nickname_check() \
            .email_check() \
            .password_check()\
            .raise_if_invalid()
        dv.validate_id(language_id)

        email , nickname , password = email.strip().lower(), nickname.strip().lower() , password.strip()

        token = await ac.register(email,nickname ,password ,language_id)
        
        return token_pb2.TokenWithText(
                success=token_pb2.TokenWithTextSuccess(
                    token=token,
                    text="Success: check your email for approval code"
                )
                )

    @RubberCatcher(True)
    @authorize()
    @not_empty('code')
    async def ApproveAccount(self, request, context,data):
        code = request.code
        cv.validate(code)

        token = await ac.check_code(data,code)

        return token_pb2.TokenWithText(
                success=token_pb2.TokenWithTextSuccess(
                    token=token,
                    text="Code is approved , now u have 2 hours to finish the registration"
                )
                )

        
    @RubberCatcher(True)
    @authorize()
    @not_empty('birthday','pronounce','sex','avatar')
    async def AdditionalInformation(self, request, context,data):
        birthday,pronounce,sex,avatar = request.birthday,request.pronounce,request.sex,request.avatar


        try:
            birthday = do.normalizer(birthday)
        except Exception as e:
            RubberException.fastRubber(f"WRONG DATA FORMAT: {e}",3)

        uv(birthday=birthday,pronounce=pronounce,sex=sex,avatar=avatar)\
            .avatar_check(data.get("_id"))\
            .pronouce_check()\
            .sex_check()\
            .birthday_check()\
            .raise_if_invalid()
        
        token = await ac.add_info(data,birthday,pronounce,sex,avatar)

        return token_pb2.TokenWithText(
                success=token_pb2.TokenWithTextSuccess(
                    token=token,
                    text="Registration is completed , u are welcome"
                )
                )


        
        