from ...data_mappers.data_mappers_repository import OrderItemMapper
from ..db_models import OrderItem
from ..repositories_db import BaseRepository


class OrderItemRepository(BaseRepository):
    model = OrderItem
    mapper = OrderItemMapper
