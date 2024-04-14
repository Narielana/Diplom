import typing as tp

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src import db
from src.api import role_post, role_get, role_put, role_delete, add_user_role
from src.models import user as user_models
from src.models import roles as roles_models
from src.utils import user as user_utils


router = APIRouter()


@router.post("/api/v1/role")
async def roles_create(
    user: tp.Annotated[user_models.UserBase, Depends(user_utils.get_current_user)],
    role: roles_models.RoleCreate,
    conn: tp.Annotated[AsyncSession, Depends(db.get_db)],
):
    return await role_post.handle(conn=conn, user=user, role=role)


@router.get("/api/v1/role")
async def roles_get(
    user: tp.Annotated[user_models.UserBase, Depends(user_utils.get_current_user)],
    conn: tp.Annotated[AsyncSession, Depends(db.get_db)],
):
    return await role_get.handle(conn=conn, user=user)


@router.put("/api/v1/role")
async def roles_put(
    user: tp.Annotated[user_models.UserBase, Depends(user_utils.get_current_user)],
    role: roles_models.RoleCreate,
    conn: tp.Annotated[AsyncSession, Depends(db.get_db)],
):
    return await role_put.handle(conn=conn, user=user, role=role)


@router.delete("/api/v1/role")
async def roles_delete(
    user: tp.Annotated[user_models.UserBase, Depends(user_utils.get_current_user)],
    key_role: str,
    conn: tp.Annotated[AsyncSession, Depends(db.get_db)],
):
    return await role_delete.handle(conn=conn, user=user, key_role=key_role)


@router.post("/api/v1/role/add")
async def add_role(
    user: tp.Annotated[user_models.UserBase, Depends(user_utils.get_current_user)],
    add_role: roles_models.AddUserRole,
    conn: tp.Annotated[AsyncSession, Depends(db.get_db)],
):
    return await add_user_role.handle(conn=conn, user=user, add_role=add_role)
