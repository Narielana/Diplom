import datetime

from fastapi import status, Response, Request
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import insert

from src.models import user as user_models
from src.utils import user as user_utils
from src.utils.oauth2 import AuthJWT


async def handle(
    request: Request,
    user: user_models.UserLogin,
    conn: AsyncSession,
    response: Response,
    Authorize: AuthJWT,
):
    user: user_models.UserBase = await user_utils.authenticate_user(
        email=user.email, password=user.password, conn=conn
    )
    if not user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Incorrect username or password"},
        )

    fingerprint = request.headers.get("X-Fingerprint-ID")
    if not fingerprint:
        raise JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Incorrect session"},
        )

    session = await user_utils.authenticate_user_session(
        fingerprint=fingerprint,
        user_id=user.id,
        conn=conn,
    )
    if not session:
        await conn.exec(
            insert(user_models.UsersSessions),
            [
                {
                    "user_id": user.id,
                    "session_id": fingerprint,
                },
            ],
        )
        await conn.commit()

    access_token = Authorize.create_access_token(
        subject=str(user.id),
        expires_time=datetime.timedelta(minutes=user_utils.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    refresh_token = Authorize.create_refresh_token(
        subject=str(user.id),
        expires_time=datetime.timedelta(
            minutes=user_utils.REFRESH_TOKEN_EXPIRE_MINUTES
        ),
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=user_utils.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        expires=user_utils.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        secure=False,
        httponly=True,
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "token": access_token,
            "token_type": "bearer",
        },
    )
