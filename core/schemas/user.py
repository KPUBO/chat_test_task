from fastapi_users import schemas, models
from pydantic import EmailStr, BaseModel


class UserRead(schemas.BaseUser[int]):
    name: str

    model_config = {
        "json_schema_extra": {
            'password': {'exclude': True},
            'is_active': {'exclude': True},
            'is_superuser': {'exclude': True},
            'is_verified': {'exclude': True},
        }
    }

class UserCreate(schemas.BaseUserCreate):
    name: str

class UserUpdate(schemas.BaseUserUpdate):
    pass

    model_config = {
        "json_schema_extra": {
            'is_active': {'exclude': True},
            'is_superuser': {'exclude': True},
            'is_verified': {'exclude': True},
        }
    }
