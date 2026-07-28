from pydantic import BaseModel, ConfigDict


class CategoriesMapper(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    parent_id: int | None
