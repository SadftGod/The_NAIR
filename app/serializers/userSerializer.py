from dataclasses import dataclass, asdict
from typing import Optional, Any, Dict
import json
from datetime import datetime , date


@dataclass(frozen=True)
class Language:
    id: int
    name: str
    abbreviation: str

@dataclass(frozen=True)
class Plan:
    # id: int
    title: str

@dataclass(frozen=True)
class Role:
    # id: int
    title: str

@dataclass(frozen=True)
class Theme:
    id: int
    name: str

@dataclass(frozen=True)
class User:
    u_id: int
    email: str
    nickname: str
    pronounce: Optional[str]
    avatar: Optional[str]
    profile_hat: Optional[str]
    sex: Optional[str]
    birthday: Optional[Any]
    status: Optional[str]
    status_until: Optional[Any]
    is_email_verified: bool
    language: Language
    plan: Plan
    role: Role
    theme: Theme

    def serialize(self,obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
    
    def get_as_json(self, indent=None):
        return json.dumps(asdict(self), ensure_ascii=False, indent=indent, default=self.serialize)

@dataclass(frozen=True)
class UserResponse:
    u_id: int
    email: str
    nickname: str
    def get_as_json(self, *, indent: int = None) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=indent)
    
@dataclass(frozen=True)
class PreUser:
    u_id: int
    email: str
    nickname: str
    language_id : int
    def get_as_json(self, *, indent: int = None) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=indent)


class UserSerializer:
    def __init__(self, data: Dict[str, Any]):
        
        self._d = data

    def serialize(self) -> User:
        lang = Language(
            id=self._d["language_id"],
            name=self._d["language_name"].title(),
            abbreviation=self._d["language_abbreviation"],
        )
        plan = Plan(
            # id=self._d["plan_id"],
            title=self._d["plan_title"],
        )
        role = Role(
            # id=self._d["role_id"],
            title=self._d["role_title"],
        )
        theme = Theme(
            id=self._d["theme_id"],
            name=self._d["theme_name"],
        )

        return User(
            u_id               = self._d["u_id"],
            email              = self._d["email"],
            nickname           = self._d["nickname"],
            pronounce          = self._d.get("pronounce"),
            avatar             = self._d.get("avatar"),
            profile_hat        = self._d.get("profile_hat"),
            sex                = self._d.get("sex"),
            birthday           = self._d.get("birthday"),
            status             = self._d.get("status"),
            status_until       = self._d.get("status_until"),
            is_email_verified  = self._d.get("is_email_verified", False),
            language           = lang,
            plan               = plan,
            role               = role,
            theme              = theme,
        )


class CodeSerializer:
    def __init__(self, data: Dict[str, Any]):
        self._d = data
        
    def serialize(self) -> UserResponse:
        return UserResponse(
            u_id               = self._d.get("_id",0),
            email              = self._d.get("email",""),
            nickname           = self._d.get("nickname",""),
        )



class CodeApproveSerializer:
    def __init__(self, data: Dict[str, Any]):
        
        self._d = data

    def serialize(self) -> User:
        return PreUser(
            u_id               = self._d["_id"],
            email              = self._d["email"],
            nickname           = self._d["nickname"],
            language_id           = self._d["language_id"]
        )