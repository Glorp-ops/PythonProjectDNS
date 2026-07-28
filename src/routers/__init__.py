from .auth_email_with_password import router as auth_email_with_password_router
from .auth_mail import router as auth_email_router
from .carts_items_router import router as carts_items_router
from .categories_router import router as categories_router
from .favorite_router import router as favorite_router
from .forgot_password import router as forgot_password_router
from .logout import router as logout_router
from .orders_router import router as orders_router
from .products_router import router as products_router
from .refresh_token import router as refresh_token_router
from .reviews_router import router as reviews_router
from .update_password import router as update_password_router
from .user_settings import router as user_settings_router

__all__ = [
    "auth_email_router",
    "auth_email_with_password_router",
    "carts_items_router",
    "categories_router",
    "favorite_router",
    "forgot_password_router",
    "logout_router",
    "orders_router",
    "products_router",
    "refresh_token_router",
    "reviews_router",
    "update_password_router",
    "user_settings_router",
]
