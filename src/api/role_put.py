from fastapi import Response, status
from fastapi.responses import JSONResponse
from sqlalchemy import update
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import user as user_models
from src.models import roles as roles_models
from src.utils import roles as roles_utils


async def handle(
    conn: AsyncSession,
    role: roles_models.RoleCreate,
    user: user_models.UserBase,
):
    if not (await roles_utils.validate_role(user_id=user.id, conn=conn, roles=[roles_utils.MASTER_ADMIN_ROLE])):
        return JSONResponse(
            content={'message': 'Access denied'},
            status_code=status.HTTP_403_FORBIDDEN,
        )

    role_base = await roles_utils.get_role(conn=conn, role=role.key_role)
    if not role_base:
        return JSONResponse(
            content={'message': 'Role does not exists'},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    query = (
        update(roles_models.RolesBase).
        where(roles_models.RolesBase.key == role.key_role).
        values(
            name = role.name,
            description = role.description
        )
    )
    await conn.exec(query)
    await conn.commit()

    return Response(status_code=200)
