import typing as tp

from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import roles as roles_models


MASTER_ADMIN_ROLE = 'master_admin'


async def validate_role(user_id: int, conn: AsyncSession, roles: tp.List[str]):
    query = select(
        roles_models.UsersRoles.id
    ).where(roles_models.UsersRoles.user_id == user_id).filter(roles_models.UsersRoles.role_key.in_(roles))
    return (await conn.exec(query)).fetchone()


async def get_role(conn: AsyncSession, role: str):
    query = select(
        roles_models.RolesBase.key,
        roles_models.RolesBase.name,
        roles_models.RolesBase.description
    ).where(roles_models.RolesBase.key == role)

    return (await conn.exec(query)).fetchone()


async def get_all_roles(conn: AsyncSession):
    query = select(
        roles_models.RolesBase.key,
        roles_models.RolesBase.name,
        roles_models.RolesBase.description
    )

    return (await conn.exec(query)).fetchall()


async def get_user_role(user_id: int, conn: AsyncSession):
    query = select(
        roles_models.UsersRoles.id
    ).where(roles_models.UsersRoles.user_id == user_id)

    return (await conn.exec(query)).fetchone()
