import re
from pydantic import BaseModel, validator


class UserBase(BaseModel):
    email: str
    password: str

    @validator('email')
    def validate_email(cls, v):
        if v is not None:
            regExs = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            if not re.fullmatch(regExs, v):
                raise ValueError("not valid email")
            return v


class UserLogin(UserBase):
    pass
