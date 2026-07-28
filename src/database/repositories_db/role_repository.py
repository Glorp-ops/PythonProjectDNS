from ...data_mappers.data_mappers_repository import RoleMapper
from ..db_models import Role
from ..repositories_db import BaseRepository


class RoleRepository(BaseRepository):
    mapper = RoleMapper
    model = Role
