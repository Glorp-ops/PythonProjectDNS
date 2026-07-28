from ...data_mappers.data_mappers_repository import CartMapper
from ..db_models import Cart
from ..repositories_db import BaseRepository


class CartRepository(BaseRepository):
    model = Cart
    mapper = CartMapper
