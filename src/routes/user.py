import typing as tp

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src import db
from src.models import user
from src.api import registry


router = APIRouter()


@router.post('/api/v1/user/registry')
async def registry_user(
    user: user.UserCreate,
    conn: tp.Annotated[AsyncSession, Depends(db.get_db)],
):
    return await registry.handle(user=user, conn=conn)
