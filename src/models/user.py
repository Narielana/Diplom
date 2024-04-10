import datetime
import typing as tp

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import (
    Column, DateTime, Integer, Text
)
from sqlalchemy_utils import EmailType, force_auto_coercion

from src import db_base

force_auto_coercion()


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    surname: str
    password: tp.Annotated[str, Field(min_length=8)]


class UserBase(db_base.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(EmailType(50), unique=True, nullable=False)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(datetime.timezone.utc))
