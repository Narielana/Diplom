import typing as tp

from fastapi import APIRouter, Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from src import db
from src.api import registry, login, me, refresh, logout, user_info, user_info_email
from src.models import user as user_models
from src.utils import user as user_utils
from src.utils.oauth2 import AuthJWT


router = APIRouter()


@router.post("/api/v1/user/registry")
async def registry_user(
    user: user_models.UserCreate,
    conn: tp.Annotated[AsyncSession, Depends(db.get_db)],
):
    return await registry.handle(user=user, conn=conn)


@router.post("/api/v1/user/login")
async def login_user(
    request: Request,
    user: user_models.UserLogin,
    conn: tp.Annotated[AsyncSession, Depends(db.get_db)],
    Authorize: tp.Annotated[AuthJWT, Depends()],
):
    return await login.handle(
        request=request, user=user, conn=conn, Authorize=Authorize
    )


@router.get("/api/v1/user/me")
async def read_users_me(
    user: tp.Annotated[user_models.UserBase, Depends(user_utils.get_current_user)],
):
    return await me.handle(
        user=user,
    )


@router.get("/api/v1/user/refresh")
async def refresh_token(
    request: Request,
    conn: tp.Annotated[AsyncSession, Depends(db.get_db)],
    Authorize: tp.Annotated[AuthJWT, Depends()],
):
    return await refresh.handle(conn=conn, request=request, Authorize=Authorize)


@router.get("/api/v1/user/logout")
async def logout_user(
    user: tp.Annotated[user_models.UserBase, Depends(user_utils.get_current_user)],
    conn: tp.Annotated[AsyncSession, Depends(db.get_db)],
    Authorize: tp.Annotated[AuthJWT, Depends()],
):
    return await logout.handle(conn=conn, user=user, Authorize=Authorize)


@router.get("/personal/v1/user_info")
async def get_user_info(
    user_id: int,
    conn: tp.Annotated[AsyncSession, Depends(db.get_db)],
):
    return await user_info.handle(user=user_id, conn=conn)


@router.get("/personal/v1/user_info/email")
async def get_user_info_email(
    email: str,
    conn: tp.Annotated[AsyncSession, Depends(db.get_db)],
):
    return await user_info_email.handle(email=email, conn=conn)
