from ...data_mappers.data_mappers_repository import (
    RolesPermissionsMapper,
)
from ..db_models import RolesPermissions
from ..repositories_db import BaseRepository


class RolesPermissionsRepository(BaseRepository):
    mapper = RolesPermissionsMapper
    model = RolesPermissions
