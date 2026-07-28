from pydantic import BaseModel, EmailStr


class AuthEmailWithPassword(BaseModel):
    email: EmailStr
    password: str
