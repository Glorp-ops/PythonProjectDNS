from pydantic import BaseModel


class EmailInfo(BaseModel):
    was_send: bool = True
    seconds_before_resending: int = 30
