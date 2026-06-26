from pydantic import BaseModel, ConfigDict


class RoleMapper(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
