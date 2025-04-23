from modules.palette import Palette as p
from modules.server_exceptions import RubberException
from app.services.passwordOperator import PasswordOperator as po
from app.services.tokenOperator import TokenOperator as to
from modules.harp import Harp
from app.database.decorators.connection import connection
from app.database.enums.db import Bases


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

        

