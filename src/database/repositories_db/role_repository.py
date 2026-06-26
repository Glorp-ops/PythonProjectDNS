from src.database.db_models.roles import Role
from src.database.repositories_db.base_repository import BaseRepository
from src.datamapers.role_mapper import RoleMapper


class RoleRepository(BaseRepository):
    mapper = RoleMapper
    model = Role
