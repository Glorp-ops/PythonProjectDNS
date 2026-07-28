from pydantic import BaseModel, ConfigDict


class RolesPermissionsMapper(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role_id: int
    permission_id: int
