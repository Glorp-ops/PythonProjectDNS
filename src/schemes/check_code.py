from pydantic import BaseModel


class CheckCode(BaseModel):
    code: str
