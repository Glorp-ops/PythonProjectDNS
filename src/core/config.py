from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from src.core.settings_mail import SettingsMail
from src.core.settings_jwt import JWTSettings

load_dotenv()


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    DB_URL: str
    REDIS_HOST: str
    REDIS_PORT: int
    AUTH_ADMIN_KEY: str

    settings_mail: BaseSettings = SettingsMail()
    settings_jwt: JWTSettings = JWTSettings()

    DEBUG: bool = False
    TESTING: bool = False

    class Config:
        env_file = "../../.env"


settings = Settings()
