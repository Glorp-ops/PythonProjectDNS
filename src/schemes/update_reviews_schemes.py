from pydantic import BaseModel, ConfigDict, Field


class UpdateReviewsScheme(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"review_id": 0, "rating": 0, "title": "", "content": ""}
        }
    )

    review_id: int
    rating: float = Field(gt=0, le=5.0)
    title: str
    content: str
