from pydantic import BaseModel, ConfigDict, Field


class ReviewsScheme(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"product_id": 0, "rating": 0, "title": "", "content": ""}
        }
    )
    product_id: int = Field(gt=0)
    rating: float = Field(gt=0, le=5.0)
    title: str
    content: str
