from typing import Any
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from ...data_mappers.data_mappers_get import GetCartItemsMapper
from ...data_mappers.data_mappers_repository import CartsItemsMapper
from ..db_models import Cart, CartItem, Product
from ..repositories_db import BaseRepository


class CartsItemsRepository(BaseRepository):
    model = CartItem
    mapper = CartsItemsMapper

    async def get_data_cart_and_cart_items(self, user_id: UUID, page: int, size: int):
        from ...data_mappers.data_mappers_get import GetProductsMapper

        count_cart_items = await self.session.scalar(
            select(func.count()).select_from(self.model)
        )

        user_cart_data = await self.session.execute(
            select(self.model, Cart.user_id)
            .join(self.model.carts)
            .where(Cart.user_id == user_id)
            .offset(size * (page - 1))
            .limit(size)
            .options(
                joinedload(self.model.products).joinedload(Product.images),
                joinedload(self.model.carts),
            )
        )

        massiv = []
        total_cart_price: float = 0
        total_items_count: int = 0
        cart_data: dict[str, Any] = {}
        cart_active: bool | None = None

        for data in user_cart_data.scalars().unique().all():
            cart_data = {"cart_id": data.cart_id, "user_id": user_id}
            try:
                image_url = data.products[0].images[0].image_url
            except IndexError:
                image_url = None

            total_cart_price += data.price_at_add * data.quantity
            total_items_count += data.quantity

            massiv.append(
                GetCartItemsMapper(
                    id=data.id,
                    price_at_add=data.price_at_add,
                    quantity=data.quantity,
                    total_price=data.total_price,
                    product=GetProductsMapper(
                        id=data.products[0].id,
                        image_url=image_url,
                        name=data.products[0].name,
                        price=data.products[0].price,
                        rating=data.products[0].rating,
                        review_count=data.products[0].review_count,
                    ),
                )
            )

            cart_active = data.carts[0].is_active

        summary = {
            "total_items_count": total_items_count,
            "total_cart_price": total_cart_price,
        }

        return (
            massiv,
            cart_data,
            summary,
            cart_active,
            {"page": page, "size": size, "all_pages": (count_cart_items // size)},
        )
