from ...data_mappers.data_mappers_repository import OrderMapper
from ..db_models import Order
from ..repositories_db import BaseRepository


class OrderRepository(BaseRepository):
    model = Order
    mapper = OrderMapper
