from pydantic import BaseModel, Field


class LikeReviewScheme(BaseModel):
    review_id: int = Field(gt=0)
