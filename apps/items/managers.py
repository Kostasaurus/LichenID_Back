
import os.path
import uuid

from fastapi import Depends, HTTPException, UploadFile, File
from sqlalchemy import insert, update, select
from sqlalchemy.exc import IntegrityError

from lichenid.S3.S3_client import S3Client
from lichenid.core.core_dependency.db_dependency import DBDependency
from lichenid.core.core_dependency.redis_dependency import RedisDependency
from lichenid.database.models.files import Files


class ItemsManager:
    def __init__(self, db: DBDependency = Depends(DBDependency), redis: RedisDependency = Depends(RedisDependency), s3: S3Client = Depends(S3Client)):
        self.db = db
        self.model = Files
        self.redis = redis
        self.s3 = s3


    async def get_object_key(self, user_id: uuid.UUID | str, object_name: str) -> str:
        async with self.db.db_session() as session:
            stmt = select(self.model.s3_key).where(
                self.model.user_id == user_id,
                self.model.object_name == object_name
            )
            s3_key = await session.scalar(stmt)
            if s3_key is None:
                raise HTTPException(status_code=404, detail="File not found")
            return s3_key


    async def upload_file(
            self,
            user_id: uuid.UUID | str,
            file: UploadFile = File(...)
    ):
        file_ext = os.path.splitext(file.filename)[1]
        s3_key = f"users/{user_id}/{uuid.uuid4()}{file_ext}"

        contents = await file.read()

        try:
            await self.s3.upload_file(
                key=s3_key,
                contents=contents,
                content_type=file.content_type
            )
        except Exception as e:
            raise HTTPException(500, f"S3 upload failed: {e}")

        async with self.db.db_session() as session:

            stmt = insert(self.model).values(
                s3_key=s3_key,
                object_name=file.filename,
                content_type=file_ext,
                user_id=user_id
            ).returning(self.model.s3_key)

            try:
                result = await session.execute(stmt)
            except IntegrityError:
                raise HTTPException(status_code=400, detail="File already exists")

            await session.commit()

            return result.scalar()


    async def update_file(self,
                          object_key: str,
                          file: UploadFile = File(...),
                          ):

            file_ext = os.path.splitext(file.filename)[1]

            contents = await file.read()

            try:

                await self.s3.upload_file(contents=contents, key=object_key, content_type=file_ext)
            except:
                raise HTTPException(status_code=500, detail="S3 problems")







