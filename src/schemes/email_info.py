from pydantic import BaseModel


class EmailInfo(BaseModel):
    wasSend: bool = True
    secondsBeforeResending: int = 30
