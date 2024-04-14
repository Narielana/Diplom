import datetime
import typing as tp

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import (
    Column, DateTime, Integer, Text, ForeignKey
)
from sqlalchemy_utils import EmailType, force_auto_coercion

from src import db_base

force_auto_coercion()


class RoleCreate(BaseModel):
    key_role: str
    name: str
    description: tp.Optional[str]


class AddUserRole(BaseModel):
    email: EmailStr
    key_role: str


class RolesBase(db_base.Base):
    __tablename__ = "roles"

    key = Column(Text, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)


class UsersRoles(db_base.Base):
    __tablename__ = "users_roles"

    id = Column(Text, primary_key=True)
    role_key = Column(Text, ForeignKey('roles.key', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
