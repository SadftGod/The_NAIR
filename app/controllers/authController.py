from modules.palette import Palette as p
from modules.server_exceptions import RubberException
from app.services.passwordOperator import PasswordOperator as po
from app.services.codeOperator import CodeOperator as co
from app.services.tokenOperator import TokenOperator as to
from modules.harp import Harp
from app.database.decorators.connection import connection
from app.database.enums.db import Bases
from datetime import  timedelta
from app.services.email import EmailBuilder,EmailSender
from dotenv import load_dotenv
import os
import asyncio
from datetime import datetime, timedelta, timezone

load_dotenv()

class AuthController:
    
    @staticmethod
    async def login(login:str,password:str) :
        user = await AuthSQLController.login(login)
        if not user:
            RubberException.fastRubber("Wrong login or password",3)
        if len(user) < 1:
            RubberException.fastRubber("Wrong login or password",3)
        if len(user) > 2:
            RubberException.fastRubber("Magic outside of hogwarts",3)

        user = user[0]
        if not po(password).compare_with(user['password']):
            RubberException.fastRubber("Wrong login or password",3)
        
        token = to(user).create_jwt()
        
        return token   

    @staticmethod
    async def register(email,nickname ,password ,language_id):
        password = po(password).encode()
        code = co.generate(6)
        data = await AuthSQLController.register(email,nickname,password,language_id,code)
        if len(data) < 1:
            RubberException.fastRubber("Registration process don't return anything",2)
        data = data[0]
        
        def send_email_task(data, code):
            name = data.get("nickname", "user").capitalize()
            html = EmailBuilder('app/templates').render(name, code)

            login = os.getenv("GOOGLE_LOGIN")
            password = os.getenv("GOOGLE_PASSWORD")

            EmailSender(
                smtp_server="smtp.gmail.com",
                smtp_port=465,
                username=login,
                password=password
            ).send_email(
                data.get("email"),
                f"NAIR email approve - code: {code}",
                html
            )
            del name, html
        asyncio.create_task(asyncio.to_thread(send_email_task, data, code))

        token = to(data).create_jwt(timedelta(minutes = 5),'code')
        return token

    @staticmethod
    async def check_code(data,code):
        req_id = data.get("_id")
        email = data.get("email")
        nickname = data.get("nickname")

        if not all([req_id, email, nickname]):
            raise RubberException.fastRubber("Wrong token: token has not enough information", 7)
        
        code_via_time = await AuthSQLController.get_true_code(req_id,email,nickname)

        if not code_via_time or len(code_via_time) < 1 :
            RubberException.fastRubber("You need to send code firstly",7)

        code_via_time = code_via_time[0]
        p.blue(code_via_time)
        code_from_db,time =  code_via_time["code"],code_via_time["created_at"]

        if code != code_from_db:
            RubberException.fastRubber("WRONG CODE: check your email again",7)

        now = datetime.now(timezone.utc).astimezone(time.tzinfo)

        difference = now - time

        if difference > timedelta(minutes=2):
            RubberException.fastRubber("Invalid code, send the request again",7)


        user_data = await AuthSQLController.get_user_from_unregistered(req_id)
        if not user_data:
            RubberException.fastRubber("Can not find ur request",5)
        user_data = user_data[0]

        token = to(user_data).create_jwt(timedelta(hours = 2),'code_approve')
        return token

    @staticmethod 
    async def add_info(data,birthday,pronounce,sex,avatar):
        email, nickname, password , language_id = data.get("email"), data.get("nickname"), data.get("password"), data.get("language_id") 
        id_to_delete = data.get("_id")
        if not all((email, nickname, password , language_id,birthday,pronounce,sex,avatar,id_to_delete)):
            RubberException.fastRubber("Not enough params",3)
        default_params = (1,1,1)
        params = (email, nickname, password , language_id,birthday,pronounce,sex,avatar) + default_params
        user = await AuthSQLController.add_info(params,id_to_delete)

        if not user:
            RubberException.fastRubber("Wrong login or password",3)
        if len(user) < 1:
            RubberException.fastRubber("Wrong login or password",3)
        if len(user) > 2:
            RubberException.fastRubber("Magic outside of hogwarts",3)

        user = user[0]
        return to(user).create_jwt()


class AuthSQLController:
    
    @staticmethod
    @connection([Bases.u.value])
    async def login(login:str,pool:dict):
        return await Harp(pool[Bases.u.value],base="users u",params = (login,login,))\
            .where("email ILIKE %s OR nickname ILIKE %s")\
            .what("u._id as u_id","u.email","u.nickname","u.password","u.pronounce","u.avatar","u.profile_hat","u.sex","u.birthday","u.status","u.status_until","u.is_email_verified","l._id as language_id","l.title as language_name","l.abbreviation as language_abbreviation","p._id as plan_id","p.title as plan_title","r._id as role_id","r.title as role_title","t._id as theme_id","t.name as theme_name") \
            .join("languages l","l._id = u.language_id")\
            .join("plans p","p._id = u.plan_id")\
            .join("role r","r._id = u.role_id")\
            .join("themes t","t._id = u.theme_id")\
            .call(req_type="select",return_type="dict")

    @staticmethod
    @connection([Bases.u.value])
    async def register(email,nickname,password,language_id,code:int,pool:dict):
        exists = await Harp(pool[Bases.u.value],"users",params = (email , nickname,))\
            .where("email = %s or nickname = %s")\
            .what("email","nickname")\
            .call("select")
        if exists and len(exists) > 0:
            RubberException.fastRubber("Account with this email or nickname was already exists",6)
        return await Harp(pool[Bases.u.value],base="unfinished_registration",params=(email,nickname,password,language_id,code,))\
            .what("email","nickname","password","language_id","code")\
            .on_conflict("update", "email", "nickname","code")\
            .returning("_id","email","nickname")\
            .call("insert","dict",True)
        
    @staticmethod
    @connection([Bases.u.value])
    async def get_true_code(req_id,email,nickname,pool):
        return await Harp(pool[Bases.u.value], "unfinished_registration",(req_id,email,nickname))\
            .what("code","created_at")\
            .where("_id = %s AND email = %s AND nickname = %s")\
            .call("select","dict")
    
    @staticmethod
    @connection([Bases.u.value])
    async def get_user_from_unregistered(req_id,pool):
        return await Harp(pool[Bases.u.value],"unfinished_registration",("A",req_id,))\
            .what("status") \
            .where("_id = %s") \
            .returning("_id","email","nickname","password","language_id")\
            .call("update","dict",True)
    
    @staticmethod
    @connection([Bases.u.value])
    async def add_info(params,id_to_delete,pool):
        cte_insert, cte_params = await Harp(pool[Bases.u.value],"users",params)\
            .what("email","nickname","password","language_id","birthday","pronounce","sex","avatar","plan_id","role_id","theme_id")\
            .returning("_id","email","nickname","password","pronounce","avatar","profile_hat","sex","birthday","status","status_until","is_email_verified","language_id","plan_id","role_id","theme_id")\
            .call("insert","dict",get=True,printed=False)        

        return await Harp(pool[Bases.u.value],base="inserted i",params = cte_params)\
           .what(
                "i._id as u_id",
                "i.email",
                "i.nickname",
                "i.password",
                "i.pronounce",
                "i.avatar",
                "i.profile_hat",
                "i.sex",
                "i.birthday",
                "i.status",
                "i.status_until",
                "i.is_email_verified",
                "l._id as language_id",
                "l.title as language_name",
                "l.abbreviation as language_abbreviation",
                "p._id as plan_id",
                "p.title as plan_title",
                "r._id as role_id",
                "r.title as role_title",
                "t._id as theme_id",
                "t.name as theme_name"
            )\
            .add_cte((cte_insert,),("inserted",))\
            .join("languages l","l._id = i.language_id")\
            .join("plans p","p._id = i.plan_id")\
            .join("role r","r._id = i.role_id")\
            .join("themes t","t._id = i.theme_id")\
            .call(req_type="select",return_type="dict",need_commit=True)