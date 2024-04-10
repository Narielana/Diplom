import typing as tp

from fastapi import APIRouter, Depends, Request, Response
from sqlmodel.ext.asyncio.session import AsyncSession

from src import db
from src.models import user
from src.api import registry, login
from src.utils.oauth2 import AuthJWT


router = APIRouter()


@router.post('/api/v1/user/registry')
async def registry_user(
    user: user.UserCreate,
    conn: tp.Annotated[AsyncSession, Depends(db.get_db)],
):
    return await registry.handle(user=user, conn=conn)


@router.post('/api//v1/user/login')
async def login_user(
    request: Request,
    user: user.UserLogin,
    conn: tp.Annotated[AsyncSession, Depends(db.get_db)],
    response: Response,
    Authorize: tp.Annotated[AuthJWT, Depends()],
):
    return await login.handle(request=request, user=user, conn=conn)