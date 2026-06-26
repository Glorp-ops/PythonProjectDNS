import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.sqlalchemy_connect.base import Base


class OTP(Base):
    __tablename__ = "OTPs"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    code_hash: Mapped[str] = mapped_column(unique=True)
    action_type: Mapped[str] = mapped_column(String(25))
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    expires_at: Mapped[datetime.datetime] = mapped_column(
        default=int(
            (datetime.datetime.now() + datetime.timedelta(minutes=5)).timestamp()
        )
    )
    attempts: Mapped[int] = mapped_column(default=0)
    is_used: Mapped[bool] = mapped_column(default=False)
