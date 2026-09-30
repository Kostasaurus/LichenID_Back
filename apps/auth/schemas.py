import datetime
import uuid
from typing import NamedTuple

from pydantic import BaseModel, Field, EmailStr


class GetUserByID(BaseModel):
    id: uuid.UUID | str

class GetUserByEmail(BaseModel):
    email: str = EmailStr

class AuthUser(GetUserByEmail):
    password: str = Field(min_length=8, max_length=128)


class CreateUser(GetUserByEmail):
    hashed_password: str

class GetUserWithIDAndEmail(GetUserByID, CreateUser):
    pass

class UserVerifySchema(GetUserByID, GetUserByEmail):
    session_id: uuid.UUID | str | None = None

class UserReturnData(GetUserByEmail, GetUserByID):
    is_verified: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class CreateTokenTuple(NamedTuple):
    encoded_jwt: str
    session_id: str


