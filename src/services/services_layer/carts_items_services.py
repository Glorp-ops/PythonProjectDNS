from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from ...database.db_models import Cart
from ...database.repositories_db import (
    CartRepository,
    CartsItemsRepository,
    ProductsRepository,
)
from ...dependencies import check_products


class CartsItemsService:
    def __init__(self, session: AsyncSession):
        self.cart_repo = CartRepository(session)
        self.cart_item_repo = CartsItemsRepository(session)
        self.product_repo = ProductsRepository(session)
        self.session = session

    async def add_cart_item(self, product_id: int, user_id: UUID):

        user_carts = await self.session.scalar(
            select(self.cart_repo.model)
            .where(
                self.cart_repo.model.user_id == user_id,
            )
            .options(joinedload(self.cart_repo.model.carts_items))
        )

        items = await self.cart_item_repo.get_filter(product_id=product_id)
        try:
            if items[0].product_id:
                await check_products(
                    product_id=items[0].product_id,
                    quantity=items[0].quantity,
                    session=self.session,
                )

            cart_items = await self.cart_item_repo.update(
                user_carts.carts_items[0].id,
                quantity=user_carts.carts_items[0].quantity + 1,
            )

            return cart_items

        except IndexError:
            pass

        if not user_carts or not user_carts.is_active:
            cart = await self.cart_repo.add(user_id=user_id)

        else:
            cart_massiv = await self.cart_repo.get_filter(user_id=user_id)
            cart = cart_massiv[0]

        product = await self.product_repo.get_filter(id=product_id)

        await check_products(
            product_id=product_id,
            session=self.session,
        )

        # try:
        #     if product[0].quantity < 1:
        #         raise HTTPException(
        #             status_code=status.HTTP_400_BAD_REQUEST,
        #             detail="This item is unavailable",
        #         )
        # except IndexError:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail="Product not found",
        #     )

        cart_items = await self.cart_item_repo.add(
            product_id=product_id,
            quantity=1,
            price_at_add=product[0].price,
            cart_id=cart.id,
        )

        return cart_items

    async def update_quantity(self, item_id: int, quantity: int, user_id: UUID):

        user_cart_data_orm_obj = await self.session.execute(
            select(self.cart_item_repo.model)
            .join(self.cart_item_repo.model.carts)
            .where(Cart.user_id == user_id)
            .options(
                joinedload(self.cart_item_repo.model.products),
                joinedload(self.cart_item_repo.model.carts),
            )
        )

        user_cart_data = user_cart_data_orm_obj.scalars().unique().all()

        if not user_cart_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

        if user_cart_data[0].products[0].quantity < quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The number of items in the cart is greater than in the store",
            )

        items = await self.session.execute(
            update(self.cart_item_repo.model)
            .values(quantity=quantity)
            .returning(self.cart_item_repo.model)
            .where(
                self.cart_item_repo.model.id == item_id,
                self.cart_item_repo.model.cart_id == user_cart_data[0].carts[0].id,
            )
        )

        cart_items = items.scalar_one_or_none()

        await self.session.commit()

        if not cart_items:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

        return cart_items

    async def delete_cart_item(self, item_id: int, user_id: UUID):

        cart = await self.cart_repo.get_filter(user_id=user_id)

        deleted_item = await self.cart_item_repo.delete(id=item_id, cart_id=cart[0].id)

        if not deleted_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

        return deleted_item

    async def delete_all_cart_items(self, user_id: UUID):
        cart = await self.cart_repo.get_filter(user_id=user_id)

        deleted_items = await self.cart_item_repo.delete(cart_id=cart[0].id)

        return deleted_items
