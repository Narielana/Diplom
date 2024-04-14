import uuid

from fastapi import Response, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete, insert
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import user as user_models
from src.models import roles as roles_models
from src.utils import roles as roles_utils
from src.utils import user as user_utils


async def handle(
    conn: AsyncSession,
    add_role: roles_models.AddUserRole,
    user: user_models.UserBase,
):
    if not (await roles_utils.validate_role(user_id=user.id, conn=conn, roles=[roles_utils.MASTER_ADMIN_ROLE])):
        return JSONResponse(
            content={'message': 'Access denied'},
            status_code=status.HTTP_403_FORBIDDEN,
        )

    role_base = await roles_utils.get_role(conn=conn, role=add_role.key_role)
    if not role_base:
        return JSONResponse(
            content={'message': 'Role does not exists'},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    
    dst_user: user_models.UserBase = await user_utils.get_user_by_email(email=add_role.email, conn=conn)
    if not dst_user:
        return JSONResponse(
            content={'message': 'User with this email does not exists'},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    user_role = await roles_utils.get_user_role(conn=conn, user_id=dst_user.id)
    if user_role:
        query = (
            delete(roles_models.UsersRoles).
            where(roles_models.UsersRoles.user_id == dst_user.id)
        )
        await conn.exec(query)
        await conn.commit()

    await conn.exec(
        insert(roles_models.UsersRoles),
        [
            {
                'id': uuid.uuid4().hex,
                'role_key': add_role.key_role,
                'user_id': dst_user.id,
            }
        ],
    )
    await conn.commit()

    return Response(status_code=201)
