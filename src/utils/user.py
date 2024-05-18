import typing as tp

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from src import db
from src.models import user as user_models
from src.utils import get_file_key


SECRET_KEY = get_file_key.get_file_by_path("~/Diplom/keys/SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 10080


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user_by_email(email: str, conn: AsyncSession) -> tp.Optional[user_models.UserBase]:
    query = select(
        user_models.UserBase.id,
        user_models.UserBase.email,
        user_models.UserBase.password,
        user_models.UserBase.first_name,
        user_models.UserBase.last_name,
        user_models.UserBase.surname,
        user_models.UserBase.created_at
    ).where(user_models.UserBase.email == email)
    return (await conn.exec(query)).fetchone()


async def get_user_by_user_id(user_id: int, conn: AsyncSession) -> tp.Optional[user_models.UserBase]:
    query = select(
        user_models.UserBase.id,
        user_models.UserBase.email,
        user_models.UserBase.password,
        user_models.UserBase.first_name,
        user_models.UserBase.last_name,
        user_models.UserBase.surname,
        user_models.UserBase.created_at
    ).where(user_models.UserBase.id == user_id)
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


async def get_current_user(
    request: Request, conn: tp.Annotated[AsyncSession, Depends(db.get_db)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = request.headers.get("Authorization")
        if token:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id: int = int(payload.get("sub"))
            if user_id is None:
                raise credentials_exception
        else:
            raise credentials_exception
    except JWTError as err:
        raise credentials_exception

    fingerprint = request.headers.get("X-Fingerprint-ID")
    if (fingerprint is None) or (
        not await authenticate_user_session(
            conn=conn, fingerprint=fingerprint, user_id=user_id
        )
    ):
        raise credentials_exception

    user: tp.Optional[user_models.UserBase] = await get_user_by_user_id(
        conn=conn, user_id=user_id
    )
    if user is None:
        raise credentials_exception

    return user
