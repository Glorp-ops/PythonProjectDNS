from sqladmin import Admin

from .base_settings_admin_models import BaseAdminSettings
from .blacklist_manage import BlackListManage
from .cart_manage import CartManage
from .carts_items_manage import CartItemManage
from .categories_manage import CategoryManage
from .favorites_manage import FavoritesManage
from .images_manage import ImageManage
from .likes_manage import LikeManage
from .orders_items_manage import OrderItemManage
from .orders_manage import OrderManage
from .permissions_manage import PermissionManage
from .products_categories_manage import ProductCategoryManage
from .products_manage import ProductManage
from .reviews_manage import ReviewManage
from .roles_manage import RoleManage
from .roles_permissions_manage import RolesPermissionsManage
from .session_manager import SessionManager
from .user_manage import UserManage
from .users_roles_manage import UserRoleManage

__all__ = [
    "BaseAdminSettings",
    "BlackListManage",
    "CartItemManage",
    "CartManage",
    "CategoryManage",
    "FavoritesManage",
    "ImageManage",
    "LikeManage",
    "OrderItemManage",
    "OrderManage",
    "PermissionManage",
    "ProductCategoryManage",
    "ProductManage",
    "ReviewManage",
    "RoleManage",
    "RolesPermissionsManage",
    "SessionManager",
    "UserManage",
    "UserRoleManage",
    "add_admin",
]


def add_admin(admin: Admin):
    admin.add_view(UserManage)
    admin.add_view(BlackListManage)
    admin.add_view(SessionManager)
    admin.add_view(ProductManage)
    admin.add_view(CategoryManage)
    admin.add_view(ImageManage)
    admin.add_view(CartManage)
    admin.add_view(CartItemManage)
    admin.add_view(FavoritesManage)
    admin.add_view(OrderManage)
    admin.add_view(OrderItemManage)
    admin.add_view(ReviewManage)
    admin.add_view(LikeManage)
    admin.add_view(RoleManage)
    admin.add_view(UserRoleManage)
    admin.add_view(PermissionManage)
    admin.add_view(RolesPermissionsManage)
    admin.add_view(ProductCategoryManage)
