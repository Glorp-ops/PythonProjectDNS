import logging
from os import getenv

from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema
from pydantic import NameEmail
from starlette import status

from ..core import settings
from ..redis_db import repo_auth_email

load_dotenv()


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

    fm = FastMail(settings.settings_mail.conf_mail)
    await fm.send_message(message)


async def validate_code(email: str, code: str, user_code: str, secret: str | None = None):

    if code == user_code:
        return
    print(code)
    attempts = await repo_auth_email.manager.get(f"auth:{email}:attempts")

    await repo_auth_email.decr(f"auth:{email}:attempts")

    logging.info(attempts)
    print(attempts)
    if attempts == "0":
        if secret:
            await repo_auth_email.manager.delete_auth_data(secret, email)

        else:
            await repo_auth_email.manager.delete_constraint(email)

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="attempts are over"
        )

    print(attempts)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid code. {int(attempts)} attempts left",
    )
