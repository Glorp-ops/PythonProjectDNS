import datetime
import logging
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

logging.info(BASE_DIR)


class JWTSettings:
    PUBLIC_KEY: Path = BASE_DIR / "jwt" / "public_key.pem"
    PRIVATE_KEY: Path = BASE_DIR / "jwt" / "private_key.pem"
    ALGORITHM: str = "ES256"
    TYPE_JWT = "JWT"
    EXPIRATION_ACCESS: int = 60 * 15
    EXPIRATION_SESSION: int = datetime.datetime.now(
        tz=datetime.UTC
    ) + datetime.timedelta(days=30)
