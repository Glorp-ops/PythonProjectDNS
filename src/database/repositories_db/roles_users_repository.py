from ...data_mappers.data_mappers_repository import UserRoleMapper
from ..db_models import UserRole
from ..repositories_db import BaseRepository


class UserRoleRepository(BaseRepository):
    mapper = UserRoleMapper
    model = UserRole
