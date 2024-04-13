from fastapi import Response, status
from sqlalchemy import delete
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import user as user_models
from src.utils.oauth2 import AuthJWT


async def handle(
    conn: AsyncSession,
    user: user_models.UserBase,
    Authorize: AuthJWT,
):
    conn.exec(
        delete(user_models.UsersSessions).where(
            user_models.UsersSessions.user_id == user.id
        )
    )
    await conn.commit()
    Authorize.unset_jwt_cookies()

    response = Response(status_code=status.HTTP_200_OK)
    return response
