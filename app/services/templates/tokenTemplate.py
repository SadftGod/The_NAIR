from datetime import datetime

from app.proto.common import token_pb2

class TokenTemplate:
    def __init__(self,token):
        self.rpco = token_pb2.JustTokenResponse(
                token = token
        )
        
    def get_rpco(self):
        return self.rpco
    
class TokenAndUserTemplate:
    def __init__(self,token,user):
      userdata = token_pb2.User(
         name = user['name'],
         email = user['email'],
         language = user['language'],
         theme = user['theme'],
         birthdate = user['birthdate'],
         credits = user['credits'],
         last_login = user['login'],
         photo_link = user['photo_link'],
         sex = user['sex'],
         pronounce = user['pronounce']
      )
        
      self.rpco = token_pb2.TokenAndUserData(
               token = token,
               user = userdata 
      )
        
        
    def get_rpco(self):
        return self.rpco
