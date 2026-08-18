from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from fastapi import status as status_code
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from starlette import status

from ...data_mappers.data_mappers_get import (
    GetOrderScheme,
    GetOrdersScheme,
    GetProductsMapper,
)
from ...data_mappers.data_mappers_repository import ProductsMapper
from ...database.db_models import OrderItem, Product
from ...database.repositories_db import (
    CartRepository,
    CartsItemsRepository,
    OrderItemRepository,
    OrderRepository,
    ProductsRepository,
)


class SystemOrderService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.orders_repo = OrderRepository(session=session)
        self.order_items_repo = OrderItemRepository(session=session)
        self.carts_items_repo = CartsItemsRepository(session=session)
        self.cart_repo = CartRepository(session=session)
        self.product_repo = ProductsRepository(session=session)

    async def create_order(
        self,
        delivery_address: str,
        delivery_method: str,
        user_id: UUID,
        products_id: list[int],
    ):
        cart_data = await self.cart_repo.get_filter(user_id=user_id)
        cart_items_data = []
        try:
            for product_id in products_id:
                cart_items_data.append(
                    await self.carts_items_repo.get_filter(
                        cart_id=cart_data[0].id, product_id=product_id
                    )
                )
        except IndexError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No items found"
            ) from e

        total_price = 0
        try:
            for data in cart_items_data:
                total_price += data[0].quantity * data[0].price_at_add
        except IndexError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No items found"
            ) from e

        order_data = await self.orders_repo.add(
            delivery_address=delivery_address,
            delivery_method=delivery_method,
            total_price=total_price,
            user_id=user_id,
        )

        order_items_data = []
        for data in cart_items_data:
            order_items_data.append(
                await self.order_items_repo.add(
                    order_id=order_data.id,
                    product_id=data[0].product_id,
                    quantity=data[0].quantity,
                    price_at_purchase=data[0].price_at_add,
                )
            )

            await self.product_repo.update_quantity(
                product_id=data[0].product_id, quantity=data[0].quantity
            )
            await self.carts_items_repo.delete(
                cart_id=cart_data[0].id, product_id=data[0].product_id
            )

        return order_items_data

    async def get_orders(self, user_id: UUID, page: int, size: int):
        count_orders = await self.session.scalar(
            select(func.count()).select_from(OrderRepository.model)
        )

        order_data_db = await self.session.execute(
            select(self.orders_repo.model)
            .where(self.orders_repo.model.user_id == user_id)
            .offset(size * (page - 1))
            .limit(size)
            .options(
                selectinload(self.orders_repo.model.order_items)
                .selectinload(OrderItem.products)
                .joinedload(Product.images)
            )
        )
        order_data = order_data_db.scalars().unique().all()
        orders_data_massiv = []
        products_data_massiv = []
        total_price: int = 0

        for data in order_data:
            for data_order_items in data.order_items:
                total_price += (
                    data.order_items[0].price_at_purchase * data.order_items[0].quantity
                )

                try:
                    image_url = data_order_items.products[0].images[0].image_url
                except IndexError:
                    image_url = None

                products_data_massiv.append(
                    GetProductsMapper(
                        id=data_order_items.products[0].id,
                        name=data_order_items.products[0].name,
                        image_url=image_url,
                        price=data_order_items.products[0].price,
                        review_count=data_order_items.products[0].review_count,
                        rating=data_order_items.products[0].rating,
                    )
                )
            orders_data_massiv.append(
                GetOrdersScheme(
                    id=data.id,
                    status=data.status,
                    total_price=data.order_items[0].price_at_purchase
                    * data.order_items[0].quantity,
                    total_items_count=data.order_items[0].quantity,
                    created_at=data.created_at,
                    products=products_data_massiv,
                )
            )

            products_data_massiv = []

        return {"items": orders_data_massiv, "order_quality": len(orders_data_massiv)}, {
            "page": page,
            "size": size,
            "all_pages": count_orders // size,
        }

    async def get_order(self, order_id: int, user_id: int):
        order_data_db = await self.session.execute(
            select(self.orders_repo.model)
            .where(
                self.orders_repo.model.id == order_id,
                self.orders_repo.model.user_id == user_id,
            )
            .options(
                joinedload(self.orders_repo.model.order_items)
                .joinedload(OrderItem.products)
                .options(
                    selectinload(Product.images), selectinload(Product.products_categories)
                ),
                joinedload(self.orders_repo.model.users),
            )
        )
        order_items: list[GetOrderScheme] = []
        order_data: dict[str, str | int | datetime] = {}
        customer: dict[str, str] = {}
        delivery: dict[str, str] = {}

        for data in order_data_db.scalars().unique().all():
            for data_order_item in data.order_items:
                order_data.update(
                    {
                        "order_id": data.id,
                        "status": data.status,
                        "created_at": data.created_at,
                    }
                )
                customer.update({"name": data.users.nickname, "email": data.users.email})
                delivery.update(
                    {"method": data.delivery_method, "address": data.delivery_address}
                )

                order_items.append(
                    GetOrderScheme(
                        price_per_item=data_order_item.price_at_purchase,
                        quantity=data_order_item.quantity,
                        total_item_price=data_order_item.quantity
                        * data_order_item.price_at_purchase,
                        product=ProductsMapper(
                            id=data_order_item.product_id,
                            name=data_order_item.products[0].name,
                            price=data_order_item.products[0].price,
                            quantity=data_order_item.products[0].quantity,
                            is_deleted=data_order_item.products[0].is_deleted,
                            sku=data_order_item.products[0].sku,
                            active_at=data_order_item.products[0].active_at,
                            rating=data_order_item.products[0].rating,
                            review_count=data_order_item.products[0].review_count,
                            created_at=data_order_item.products[0].created_at,
                            categories=[
                                data.category_id
                                for data in data_order_item.products[0].products_categories
                            ],
                            description=data_order_item.products[0].description,
                            images_url=[
                                image.image_url for image in data_order_item.products[0].images
                            ],
                        ),
                    )
                )

        return {
            "order_data": order_data,
            "customer": customer,
            "delivery": delivery,
            "items": order_items,
        }

    async def update_check_delivery_status(self, order_id: int, status: str, user_id: UUID):
        status_product_id_db = await self.session.execute(
            select(self.orders_repo.model)
            .where(
                self.orders_repo.model.id == order_id,
                self.orders_repo.model.user_id == user_id,
            )
            .options(joinedload(self.orders_repo.model.order_items))
        )

        status_product_id = status_product_id_db.scalars().unique().all()

        try:
            if status_product_id[0].status == "отменен":
                return status_product_id[0].status
        except IndexError as e:
            raise HTTPException(
                status_code=status_code.HTTP_404_NOT_FOUND, detail="Order not found"
            ) from e

        stmt = await self.session.execute(
            update(self.orders_repo.model)
            .values(status=status)
            .where(
                self.orders_repo.model.id == order_id,
                self.orders_repo.model.user_id == user_id,
            )
            .options(selectinload(self.orders_repo.model.order_items))
            .returning(self.orders_repo.model)
        )

        status_order_items = stmt.scalars().all()

        await self.session.commit()

        if status_order_items[0].status == "отменен":
            for items in status_order_items[0].order_items:
                product = await self.session.get(self.product_repo.model, items.product_id)

                if not product:
                    raise HTTPException(
                        status_code=status_code.HTTP_404_NOT_FOUND,
                        detail="Product not found",
                    )

                product.quantity += items.quantity

                await self.session.commit()
                await self.session.refresh(product)
