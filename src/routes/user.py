import typing as tp

from fastapi import APIRouter, Depends, Request, Response
from sqlmodel.ext.asyncio.session import AsyncSession

from src import db
from src.api import registry, login, me
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


@router.post("/api//v1/user/login")
async def login_user(
    request: Request,
    user: user_models.UserLogin,
    conn: tp.Annotated[AsyncSession, Depends(db.get_db)],
    response: Response,
    Authorize: tp.Annotated[AuthJWT, Depends()],
):
    return await login.handle(
        request=request, user=user, conn=conn, response=response, Authorize=Authorize
    )


@router.get("/api/v1/user/me")
async def read_users_me(
    user: tp.Annotated[user_models.UserBase, Depends(user_utils.get_current_user)],
):
    return await me.handle(
        user=user,
    )
