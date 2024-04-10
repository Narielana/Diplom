from fastapi import status
from fastapi.responses import JSONResponse

from src.models import user as user_models


async def handle(
    user: user_models.UserBase,
):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "surname": user.surname,
        },
    )
