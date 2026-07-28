from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserData(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": {"name": "", "surname": "", "nickname": "", "email": ""}}
    )

    name: str | None = Field(default=None, max_length=30)
    surname: str | None = Field(default=None, max_length=30)
    nickname: str | None = Field(default=None, max_length=30)
    email: EmailStr | None = Field(default=None)

    @field_validator("*", "nickname", "email", mode="before")
    def empty_to_none(cls, v):  # noqa: N805
        if v == "":
            return None
        return v
