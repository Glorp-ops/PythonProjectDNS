import logging
from os import getenv
from random import randint

from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema
from pydantic import NameEmail
from starlette import status

from src.core.config import settings
from src.core.config import settings as conf
from src.redis_db.repositories_redis.redis_auth_email import repo_auth_email

load_dotenv()


async def random_code():
    return str(randint(1000, 9999))


async def send_email(recipients: list[NameEmail], code: str):

    logging.info(getenv("MAIL_USERNAME"))
    logging.info(getenv("MAIL_FROM"))
    logging.info(int(getenv("MAIL_PORT")))
    logging.info(getenv("MAIL_SERVER"))
    logging.info(bool(getenv("MAIL_STARTTLS")))
    logging.info(bool(getenv("MAIL_SSL_TLS")))

    message = MessageSchema(
        subject=settings.settings_mail.SUBJECT,
        recipients=recipients,
        body=code,
        subtype=settings.settings_mail.SUBTYPE,
    )

    fm = FastMail(conf.settings_mail.conf_mail)
    await fm.send_message(message)


async def validate_code(email: str, code: str, user_code: str):

    if code == user_code:
        return

    await repo_auth_email.incr(f"auth:{email}:attempts")
    attempts = await repo_auth_email.manager.get(f"auth:{email}:attempts")
    logging.info(attempts)

    if attempts == "5":
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="attempts are over"
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid code.{5 - int(attempts)} attempts left",
    )
