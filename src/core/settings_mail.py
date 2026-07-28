from os import getenv

from dotenv import load_dotenv
from fastapi_mail.config import ConnectionConfig
from pydantic import SecretStr
from pydantic_settings import BaseSettings

load_dotenv()


class SettingsMail(BaseSettings):
    SUBJECT: str = "Code Authentication"
    SUBTYPE: str = "plain"

    _MAIL_CONF = ConnectionConfig(
        MAIL_USERNAME=getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=SecretStr(getenv("APP_PASSWORD")),
        MAIL_FROM=getenv("MAIL_FROM"),
        MAIL_PORT=int(getenv("MAIL_PORT")),
        MAIL_SERVER=getenv("MAIL_SERVER"),
        MAIL_STARTTLS=bool(getenv("MAIL_STARTTLS")),
        MAIL_SSL_TLS=bool(getenv("MAIL_SSL_TLS").lower() == "true"),
        USE_CREDENTIALS=bool(getenv("USE_CREDENTIALS")),
    )

    @property
    def conf_mail(self) -> ConnectionConfig:
        return self._MAIL_CONF
