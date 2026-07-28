from ...data_mappers.data_mappers_repository import PermissionMapper
from ..db_models import Permission
from ..repositories_db import BaseRepository


class PermissionRepository(BaseRepository):
    mapper = PermissionMapper
    model = Permission
