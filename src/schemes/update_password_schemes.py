from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class UpdatePasswordCode(BaseModel):
    code: str


class UpdatePassword(BaseModel):
    password: Annotated[
        str,
        Field(
            description="Пароль должен содержать от 8 символов, "
            "включая заглавные и строчные буквы, цифры и спецсимволы.",
        ),
    ]

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:

        if len(value) < 8:
            raise ValueError("Пароль должен быть не менее 8 символов в длину.")

        if not any(c.islower() for c in value):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву.")
        if not any(c.isupper() for c in value):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву.")
        if not any(c.isdigit() for c in value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру.")

        special_chars = "@$!%*?&"
        if not any(c in special_chars for c in value):
            raise ValueError(
                f"Пароль должен содержать хотя бы один спецсимвол из набора: {special_chars}"
            )

        return value
