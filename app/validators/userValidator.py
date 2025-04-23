from modules.server_exceptions import RubberException
import re
import dns.resolver

class UserValidator:
    def __init__(self,
                 nick:str = None,
                 email:str = None,
                 password:str = None,
                 login:str = None
                 ):
        self.login = login
        self.nick = nick
        self.email = email

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
    
    
    def raise_if_invalid(self):
        if self.errors:
            RubberException.fastRubber(", ".join(self.errors), 3)