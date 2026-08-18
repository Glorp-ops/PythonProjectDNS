from datetime import UTC, datetime
from uuid import UUID

from fastapi import HTTPException, Request
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, with_loader_criteria
from starlette import status

from ..database.repositories_db import BlackListRepository, UserRepository
from ..services.encode_decode_get_put_jwt_data_auth import (
    get_jwt_data_auth_cookie,
)


async def check_ban_until(session: AsyncSession, user_id: int):
    user_blacklist = await BlackListRepository(session).get_id(user_id)

    if (user_blacklist is not None and user_blacklist.ban_until is not None) and (
        user_blacklist.ban_until < datetime.now(UTC)
    ):
        await BlackListRepository(session).delete(user_id=user_id)
        await UserRepository(session).update(user_id, is_blocked=False)


async def check_role_permission(
    session: AsyncSession, user_id: UUID, permission: str, for_admin: bool = False
):
    from ..database.repositories_db import (
        PermissionRepository,
        RoleRepository,
        RolesPermissionsRepository,
        UserRoleRepository,
    )

    roles_data_db = await session.execute(
        select(RoleRepository.model).options(
            selectinload(RoleRepository.model.users_roles),
            with_loader_criteria(
                UserRoleRepository.model,
                UserRoleRepository.model.user_id == user_id,
                include_aliases=True,
            ),
        )
    )

    roles_data = roles_data_db.scalars().all()

    roles = [data.users_roles for data in roles_data]
    user_roles = []

    for data in roles:
        if data:
            user_roles.append(data[0].role_id)

    user_parents_id = []

    for data in roles_data:
        if (data.id in user_roles) and (data.parent_id):
            user_parents_id.append(data.parent_id)

    parent_id = 0
    parents_id: list = user_parents_id.copy()

    for user_parent_id in user_parents_id:
        for data in roles_data:
            if data.id == user_parent_id:
                parent_id = data.parent_id
                parents_id.append(parent_id)
                while parent_id is not None:
                    for data in roles_data:
                        if data.id == parent_id:
                            parent_id = data.parent_id
                            parents_id.append(parent_id)

    role_data_db = await session.execute(
        select(
            RoleRepository.model,
        )
        .join(RolesPermissionsRepository.model)
        .join(PermissionRepository.model)
        .where(
            PermissionRepository.model.name == permission,
            or_(
                RoleRepository.model.id.in_(user_roles),
                RoleRepository.model.id.in_(parents_id),
            ),
        )
        .options(
            joinedload(RoleRepository.model.roles_permissions).joinedload(
                RolesPermissionsRepository.model.permissions
            )
        )
    )

    role_data = role_data_db.scalars().unique().all()

    has_permissions = bool(
        role_data
        and role_data[0].roles_permissions
        and role_data[0].roles_permissions[0].permissions
    )

    if not has_permissions:
        if not for_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have the right to do this.",
            )
        return False

    return roles_data


async def check_users_sessions(
    session: AsyncSession,
    request: Request,
    permission: str | None = None,
    refresh_token: bool = False,
    user_id_from_session: UUID | None = None,
):
    from src.dependencies.validation import (
        validate_check_session,
        validate_payload,
    )

    from ..dependencies import (
        check_active,
        check_block,
        check_exp_sessions,
        check_revoked,
    )

    auth_data = get_jwt_data_auth_cookie(request=request)

    if not refresh_token:
        payload_validate = validate_payload(auth_data["access_token"])
        user_id = payload_validate.userId

    else:
        user_id = user_id_from_session
        payload_validate = None

    await check_active(session=session, user_id=user_id)
    await check_ban_until(session, user_id)
    await check_block(session=session, user_id=user_id)
    await check_revoked(auth_public_uid=auth_data["auth_public_uid"], session=session)
    if permission:
        await check_role_permission(session, user_id=user_id, permission=permission)

    await validate_check_session(
        session,
        auth_public_uid=auth_data["auth_public_uid"],
        auth_ssid=auth_data["auth_ssid"],
        refresh_token=auth_data["auth_refresh_token"],
    )

    await check_exp_sessions(session=session, auth_public_uid=auth_data["auth_public_uid"])

    return payload_validate, auth_data
