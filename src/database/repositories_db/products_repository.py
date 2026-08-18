from sqlalchemy import func, select
from sqlalchemy.orm import joinedload, load_only, selectinload

from ...data_mappers.data_mappers_get import GetProductsMapper
from ...data_mappers.data_mappers_repository import ProductsMapper
from ..db_models import Product, ProductCategory
from ..repositories_db import BaseRepository


class ProductsRepository(BaseRepository):
    model = Product
    mapper = ProductsMapper

    async def get_products_category(self, category_id: int, size: int, page: int):

        count_products = await self.session.scalar(select(func.count()).select_from(Product))

        products_category_db = await self.session.scalars(
            select(Product)
            .join(ProductCategory)
            .offset((page - 1) * size)
            .limit(size)
            .where(ProductCategory.category_id == category_id)
            .options(joinedload(Product.images))
        )

        products_category_massiv = []

        for product in products_category_db.unique():
            try:
                image_url = product.images[0].image_url
            except IndexError:
                image_url = None

            products_category_massiv.append(
                GetProductsMapper(
                    id=product.id,
                    image_url=image_url,
                    name=product.name,
                    price=product.price,
                    review_count=product.review_count,
                    rating=product.rating,
                )
            )

        return products_category_massiv, {
            "page": page,
            "size": size,
            "all_pages": (count_products // size),
        }

    async def get_all_with_join_no_description(self, page: int, size: int):
        count_products = await self.session.scalar(select(func.count()).select_from(Product))

        products_db = (
            select(self.model)
            .offset(size * (page - 1))
            .limit(size)
            .options(
                load_only(
                    self.model.id,
                    self.model.name,
                    self.model.price,
                    self.model.review_count,
                    self.model.rating,
                ),
                selectinload(self.model.images),
            )
        )

        products = await self.session.scalars(products_db)

        massiv = []

        for product in products:
            try:
                image_url = product.images[0].image_url
            except IndexError:
                image_url = None

            massiv.append(
                GetProductsMapper(
                    id=product.id,
                    image_url=image_url,
                    name=product.name,
                    price=product.price,
                    review_count=product.review_count,
                    rating=product.rating,
                )
            )

        return massiv, {"page": page, "size": size, "page_all": count_products // size}

    async def get_id_with_join_and_description(self, product_id):

        product_db = await self.session.execute(
            (select(self.model).where(self.model.id == product_id)).options(
                selectinload(self.model.products_categories), selectinload(self.model.images)
            )
        )

        product = product_db.scalar_one()

        return self.mapper(
            id=product.id,
            images_url=[data.image_url for data in product.images],
            name=product.name,
            sku=product.sku,
            description=product.description,
            price=product.price,
            quantity=product.quantity,
            created_at=product.created_at,
            is_deleted=product.is_deleted,
            active_at=product.active_at,
            review_count=product.review_count,
            rating=product.rating,
            categories=[data.category_id for data in product.products_categories],
        )

    async def update_quantity(self, product_id: int, quantity: int):
        smt = select(self.model).where(self.model.id == product_id).with_for_update()

        product = await self.session.execute(smt)

        product.scalar_one().quantity -= quantity

        await self.session.commit()
