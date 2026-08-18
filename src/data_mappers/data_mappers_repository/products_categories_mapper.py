from pydantic import BaseModel, ConfigDict


class ProductCategoryMapper(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    category_id: int
