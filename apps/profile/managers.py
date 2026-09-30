import uuid
from typing import Any
from fastapi import Depends
from sqlalchemy import update, select

from lichenid.core.core_dependency.db_dependency import DBDependency
from lichenid.database.models.user import User

class ProfileManager:
    def __init__(self, db: DBDependency = Depends(DBDependency)):
        self.db = db
        self.model = User


    async def update_user_fields(self, user_id: uuid.UUID | str, **kwargs: Any):
        async with self.db.db_session() as session:
            stmt = update(self.model).where(self.model.id == user_id).values(**kwargs)
            await session.execute(stmt)
            await session.commit()

    async def get_user_hashed_password(self, user_id: uuid.UUID | str) -> str | None:
        async with self.db.db_session() as session:
            query = (
                select(self.model.hashed_password)
                .where(self.model.id == user_id)
            )
            result = await session.execute(query)
            return result.scalar()