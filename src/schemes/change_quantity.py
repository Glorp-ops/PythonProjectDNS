from pydantic import BaseModel, Field


class ChangeQuantity(BaseModel):
    item_id: int
    quantity: int = Field(gt=0)
