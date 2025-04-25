from modules.palette import Palette as p
from modules.scyber import Scyber
import os
import jwt
from datetime import datetime, timezone, timedelta
import json
from app.serializers.userSerializer import UserSerializer , CodeSerializer
from modules.server_exceptions import RubberException 

class TokenOperator:
    KEY_DIR  = os.path.join("app", "configs", "security")
    KEY_PATH = os.path.join(KEY_DIR, "scyber_key")

    JWT_SECRET    = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = "HS256"
    

    def __init__(self, data: dict = None):
        self.data = data
        self.key  = self._generate_master_key()

    def _generate_master_key(self) -> bytes:
        if not os.path.isdir(self.KEY_DIR):
            os.makedirs(self.KEY_DIR, exist_ok=True)
        if os.path.isfile(self.KEY_PATH):
            with open(self.KEY_PATH, "rb") as f:
                key = f.read()
            if len(key) != 32:
                raise ValueError(f"Master key must be 32 bytes, got {len(key)}")
            return key

        key = Scyber.generate_master_key()
        with open(self.KEY_PATH, "wb") as f:
            f.write(key)
        return key

    def create_jwt(self,time_to_wait:timedelta=timedelta(hours=1),jwt_type:str = 'user') -> str:
        raw = json.dumps(self.data).encode("utf-8")
        encoded_data = Scyber(raw).encode(master_key=self.key)
        
        jwt_type = jwt_type.strip().lower()
        possible_jwt_types = ['user','code']

        if not jwt_type in possible_jwt_types:
            RubberException.fastRubber(f"WRONG JWT TOKEN TYPE: use one of {' ,'.join(possible_jwt_types)}")
        
        match jwt_type:
            case 'user':
                user_json = UserSerializer(self.data).serialize().get_as_json()
            case 'code':
                user_json = CodeSerializer(self.data).serialize().get_as_json()

        user_dict = json.loads(user_json)

        now = datetime.now(timezone.utc)
        payload = {
            "data": encoded_data,
            "user": user_dict,
            "iat":  now,
            "exp":  now + time_to_wait,
        }

        token = jwt.encode(
            payload,
            self.JWT_SECRET,
            algorithm=self.JWT_ALGORITHM
        )
        return token


    def decode_jwt(self, token: str, associated_data: bytes = None) -> dict:
        payload = jwt.decode(
            token,
            self.JWT_SECRET,
            algorithms=[self.JWT_ALGORITHM],
            options={"require": ["iat", "exp"]}
        )

        encrypted = payload.get("data")
        user_dict = payload.get("user")

        decrypted_bytes = Scyber.decode(
            encrypted,
            master_key=self.key,
            associated_data=associated_data
        )

        data_dict = json.loads(decrypted_bytes.decode("utf-8"))

        return {
            "data": data_dict,
            "user": user_dict
        }
    