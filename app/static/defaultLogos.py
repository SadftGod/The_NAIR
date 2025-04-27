from enum import Enum

class AvatarEnum(str, Enum):
    DEFAULT = "app/static/logos/default_avatar.png"


    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in (item.value for item in cls)
