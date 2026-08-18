from pydantic import BaseModel, ConfigDict


class GetProductsMapper(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_url: str | None
    name: str
    price: float
    review_count: int
    rating: float
