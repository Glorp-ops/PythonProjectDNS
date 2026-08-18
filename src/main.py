import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware
from uvicorn import run

from .admin import add_admin
from .admin.auth_admin import authentication_backend
from .core import settings
from .database.sqlalchemy_connect import async_session
from .redis_db import redis_manager
from .routers import (
    auth_email_router,
    auth_email_with_password_router,
    carts_items_router,
    categories_router,
    favorite_router,
    forgot_password_router,
    logout_router,
    orders_router,
    products_router,
    refresh_token_router,
    reviews_router,
    update_password_router,
    user_settings_router,
)

logging.basicConfig(level=logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):

    await redis_manager.connect()
    logging.info(" redis connected")
    FastAPICache.init(RedisBackend(redis_manager.redis))

    yield

    await redis_manager.close()
    logging.info(" redis disconnected")


app = FastAPI(lifespan=lifespan)

app.add_middleware(SessionMiddleware, secret_key=settings.AUTH_ADMIN_KEY, max_age=86400)

admin = Admin(app, session_maker=async_session, authentication_backend=authentication_backend)
add_admin(admin)


app.include_router(auth_email_router)
app.include_router(user_settings_router)
app.include_router(refresh_token_router)
app.include_router(logout_router)
app.include_router(update_password_router)
app.include_router(auth_email_with_password_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(carts_items_router)
app.include_router(orders_router)
app.include_router(reviews_router)
app.include_router(favorite_router)
app.include_router(forgot_password_router)

if __name__ == "__main__":
    run(app, proxy_headers=True, forwarded_allow_ips="*", port=8000)
