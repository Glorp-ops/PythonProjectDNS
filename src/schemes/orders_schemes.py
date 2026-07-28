from pydantic import BaseModel


class OrdersScheme(BaseModel):
    products_id: list[int]
    delivery_address: str = "г. Москва, ул. Ленина, д. 1, кв. 42"  # noqa:RUF001
    delivery_method: str = "Лошади"
