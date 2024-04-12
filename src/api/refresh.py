import datetime
import typing as tp

from fastapi import HTTPException, status, Response, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import MissingTokenError
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import user as user_models
from src.utils import user as user_utils
from src.utils.oauth2 import AuthJWT


async def handle(
    conn: AsyncSession,
    request: Request,
    Authorize: AuthJWT,
):
    user_id: tp.Optional[int] = None

    try:
        Authorize.jwt_refresh_token_required()
        user_id = int(Authorize.get_jwt_subject())
    except MissingTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please provide refresh token",
        )
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not refresh access token",
        )

    user: user_models.UserBase = await user_utils.get_user_by_user_id(
        user_id=user_id, conn=conn
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User doesn't exists"
        )

    fingerprint = request.headers.get("X-Fingerprint-ID")
    if (fingerprint is None) or not (
        await user_utils.authenticate_user_session(
            conn=conn, fingerprint=fingerprint, user_id=user_id
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect session",
        )

    access_token = Authorize.create_access_token(
        subject=str(user.id),
        expires_time=datetime.timedelta(minutes=user_utils.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "token": access_token,
            "token_type": "bearer",
        },
    )
