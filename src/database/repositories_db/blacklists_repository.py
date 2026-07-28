from ...data_mappers.data_mappers_repository import BlacklistMapper

from ..db_models import Blacklist
from .base_repository import BaseRepository


class BlackListRepository(BaseRepository):
    mapper = BlacklistMapper
    model = Blacklist
