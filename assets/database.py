import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text
from config import settings

sync_engine = create_engine(
    url=settings.DB_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

async_engine = create_async_engine(
    url=settings.postgres_url,
    echo=False
)


async def add_user(
        username: str,
        email: str,
        password: str
):
    async with async_engine.begin() as conn:
        stmt = f"""
INSERT INTO USERS (username, email, password)
VALUES ('{username}', '{email}', '{password}')
    """
        # params = (username, email, password)

        await conn.execute(statement=text(stmt))




# session_factory = sessionmaker(sync_engine)
# new_session = async_sessionmaker(async_engine)
#

# async def get_session():
#     async with new_session as session:
#         yield session
#
# class Base(DeclarativeBase):
#     pass
#
# class UsersModel(Base):
#     __tablename__ = 'users'

asyncio.run(add_user('kostya', 'email', 'good'))

