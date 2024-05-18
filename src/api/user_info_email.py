from fastapi import status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from src.utils import user as user_utils
from src.utils import roles as roles_utils


async def handle(
    email: str,
    conn: AsyncSession,
):
    user = await user_utils.get_user_by_email(email=email, conn=conn)
    user_role = await roles_utils.get_user_role(user_id=user.email, conn=conn)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "surname": user.surname,
            "roles": [user_role] if user_role else [],
        },
    )
