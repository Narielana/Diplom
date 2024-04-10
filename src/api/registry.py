from fastapi import status, Response
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import insert

from src.models import user as user_models
from src.utils import user as user_utils


async def handle(user: user_models.UserCreate, conn: AsyncSession):
    created_user = await user_utils.get_user_by_email(email=user.email, conn=conn)
    if created_user:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={'message': 'Incorrect or expired email code'},
        )
    
    await conn.exec(
        insert(user_models.UserBase),
        [
            {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'surname': user.surname,
                'password': user_utils.get_password_hash(password=user.password),
            }
        ]
    )
    await conn.commit()

    return Response(status_code=status.HTTP_201_CREATED)
