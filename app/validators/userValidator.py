from modules.server_exceptions import RubberException
from modules.palette import Palette as p
from app.services.imageOperator import ImageOperator
from app.static.defaultLogos import AvatarEnum
from PIL import Image
from io import BytesIO

import os
import re
import base64

import dns.resolver
from datetime import datetime, timezone 

class UserValidator:
    def __init__(self,
                 nick:str = None,
                 email:str = None,
                 password:str = None,
                 login:str = None,
                 birthday:datetime  = None,
                 pronounce:str  = None,
                 sex:str  = None,
                 avatar:str  = None
                 ):
        self.login = login
        self.nick = nick
        self.email = email

        self.sex = sex 
        self.avatar = avatar
        self.pronounce = pronounce
        self.birthday = birthday

        self.password = password

        self.errors = []


    def password_check(self):
        password = self.password
        if not isinstance(password,str):
            self.errors.append("Password must a string")
            return self
        
        password = password.strip()
        
        if len(self.password) < 8:
            self.errors.append("Password must be at least 8 characters long")
        if not re.search(r"[A-Za-z]", password):
            self.errors.append("Password must contain at least one letter")
        if not re.search(r"\d", password):
            self.errors.append("Password must contain at least one digit")
        

        return self
    
    def nickname_check(self):
        nickname = self.nick
        if not isinstance(nickname,str):
            self.errors.append("Nickname must a string")
            return self
        
        nickname = nickname.strip()

        if len(nickname) <= 2:
            self.errors.append("Nickname must be longer than 2 characters")

        if not re.fullmatch(r"[A-Za-z0-9_]+", nickname):
            self.errors.append("Nickname must contain only Latin letters, digits, or underscores")

        return self
    
    def email_check(self):
        email = self.email

        if not isinstance(email, str):
            self.errors.append("Email must be a string")
            return self

        email = email.strip()

        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, email):
            self.errors.append("Email format is invalid")
            return self 
        
        domain = email.split("@")[-1]

        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            if not mx_records:
                self.errors.append(f"Email domain '{domain}' has no MX records")
        except Exception:
            self.errors.append(f"Email domain '{domain}' is not valid or has no MX")

        return self
                       
    def nick_or_email(self):
        login = self.login.strip()
        if not login or not isinstance(login,str):
            self.errors.append("Login must be a non-empty string")
            return self
        
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        is_email = re.fullmatch(email_pattern, login) is not None

        
        if is_email:
            domain = login.split("@")[-1]
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                if not mx_records:
                    self.errors.append(f"Email domain '{domain}' has no MX records")
            except Exception:
                self.errors.append(f"Email domain '{domain}' is not valid or has no MX")
        else:
            if len(login) <= 2:
                self.errors.append("Nickname must be longer than 2 characters")

            if not re.fullmatch(r"[A-Za-z0-9_]+", login):
                self.errors.append("Nickname must contain only Latin letters, digits, or underscores")

        return self
    
    def sex_check(self):
        if not isinstance(self.sex,str):
            self.errors.append("Sex might be a string format")
            return self

        if len(self.sex) != 1:
            self.errors.append("Sex might be CHAR format")
            return self


        possible_sex = {"M", "F"}

        if not self.sex.upper() in possible_sex:
            self.errors.append("there's no such sex. Pick from male('M') and female('F')")
        return self

    def pronouce_check(self):
        pronounce = self.pronounce
        if not isinstance(pronounce,str):
            self.errors.append("Pronounce must a string")
            return self
        
        pronounce = pronounce.strip()

        if len(pronounce) <= 2:
            self.errors.append("Pronounce must be longer than 2 characters")

        if not re.fullmatch(r"[A-Za-zА-Яа-яЁёІіЇїЄєҐґ0-9_ ]+", pronounce):
            self.errors.append("Pronounce must contain only Latin, Cyrillic (Russian and Ukrainian) letters, digits, underscores, or spaces")

        if "  " in pronounce:
            self.errors.append("Pronounce must not contain multiple consecutive spaces")
        return self
    
    def calculate_age(self,birthday: datetime, now: datetime = None) -> int:
        if now is None:
            now = datetime.now(timezone.utc)
        
        age = now.year - birthday.year
        if (now.month, now.day) < (birthday.month, birthday.day):
            age -= 1
        return age
    
    def birthday_check(self):
        if not isinstance(self.birthday,datetime):
            self.errors.append("Birthday might be a datetime obj")
            return self

        now = datetime.now(timezone.utc)
        if self.birthday > now:
            self.errors.append("Birthday cannot be in the future")
            return self
        
        age = self.calculate_age(self.birthday, now)

        min_age = 2
        max_age = 101

        if age < min_age:
            self.errors.append(f"User must be at least {min_age} years old")
            return self

        if age > max_age:
            self.errors.append(f"User cannot be older than {max_age} years")
        
        return self
    
    def avatar_check(self,user_id:int):
        if not isinstance(self.avatar, str):
            self.errors.append("Avatar must be a string")
            return self
        with_path = os.path.join("app/static/logos",f"{self.avatar}.png")
        if AvatarEnum.has_value(with_path):
            return self
        
        try:
            header, encoded = self.avatar.split(",", 1) if "," in self.avatar else ("", self.avatar)
            decoded = base64.b64decode(encoded, validate=True)
        except Exception:
            self.errors.append("Avatar must be a valid base64 string or known filename")
            return self

        max_size_bytes = 2 * 1024 * 1024
        if len(decoded) > max_size_bytes:
            self.errors.append("Avatar file size must not exceed 2MB")
            return self
        
        try:
            image = Image.open(BytesIO(decoded))
            image.verify() 
            image = Image.open(BytesIO(decoded)) 
        except Exception:
            self.errors.append("Avatar must be a valid image")
            return self
        

        max_width = 512
        max_height = 512
        if image.width > max_width or image.height > max_height:
            self.errors.append(f"Avatar must not exceed {max_width}x{max_height} pixels")
            return self
        
        if user_id is None:
            self.errors.append("Cannot save avatar without user ID")
            return self
        
        saved_path = ImageOperator.save_avatar(image, user_id)
        self.saved_avatar_path = saved_path





        

        return self
    def raise_if_invalid(self):
        if self.errors:
            RubberException.fastRubber(", ".join(self.errors), 3)