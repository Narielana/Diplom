import typing as tp

from passlib.context import CryptContext
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from src.models import user as user_models
from src import db


ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 10080


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user_by_email(email: str, conn: AsyncSession):
    query = select(user_models.UserBase).where(user_models.UserBase.email == email)
    return (await conn.exec(query)).fetchone()


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


async def authenticate_user(email: str, password: str, conn: AsyncSession):
    user: user_models.UserBase = await get_user_by_email(email=email, conn=conn)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_session(user_id: int, fingerprint: str, conn: AsyncSession):
    query = select(
        user_models.UsersSessions.user_id, user_models.UsersSessions.session_id
    ).where(
        user_models.UsersSessions.user_id == user_id,
        user_models.UsersSessions.session_id == fingerprint,
    )
    return (await conn.exec(query)).fetchone()


async def authenticate_user_session(fingerprint: str, user_id: int, conn: AsyncSession):
    session = await get_session(user_id=user_id, fingerprint=fingerprint, conn=conn)
    return session is not None
