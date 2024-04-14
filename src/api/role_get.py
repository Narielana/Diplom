import typing as tp

from fastapi import status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import user as user_models
from src.models import roles as roles_models
from src.utils import roles as roles_utils


async def handle(
    conn: AsyncSession,
    user: user_models.UserBase,
):
    if not (await roles_utils.validate_role(user_id=user.id, conn=conn, roles=[roles_utils.MASTER_ADMIN_ROLE])):
        return JSONResponse(
            content={'message': 'Access denied'},
            status_code=status.HTTP_403_FORBIDDEN,
        )

    roles: tp.List[roles_models.RolesBase] = await roles_utils.get_all_roles(conn=conn)

    return JSONResponse(
        status_code=200,
        content={
            'items': [
                {
                    'key': role.key,
                    'name': role.name,
                    'description': role.description,
                }
                for role in roles
            ]
        }
    )
