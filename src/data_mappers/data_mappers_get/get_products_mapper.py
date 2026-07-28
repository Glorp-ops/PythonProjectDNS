from pydantic import BaseModel


class GetProductsMapper(BaseModel):
    id: int
    image_url: str | None
    name: str
    price: float
    review_count: int
    rating: float
