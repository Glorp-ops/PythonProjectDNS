from pydantic import BaseModel, NameEmail


class AuthEmail(BaseModel):
    recipients: list[NameEmail]
