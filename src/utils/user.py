import typing as tp

from passlib.context import CryptContext
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from src.models import user as user_models
from src import db


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def get_user_by_email(email: str, conn: AsyncSession):
    query = select(user_models.UserBase).where(user_models.UserBase.email == email)
    return (await conn.exec(query)).fetchone()


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)
