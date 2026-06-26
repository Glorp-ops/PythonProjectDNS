import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.redis_db.repositories_redis.redis_manager import redis_manager
from src.routers.auth_mail import router as auth_email_router

logging.basicConfig(level=logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):

    await redis_manager.connect()
    logging.info(" redis connected")

    yield

    await redis_manager.close()
    logging.info(" redis disconnected")


app = FastAPI(lifespan=lifespan)
app.include_router(auth_email_router)
