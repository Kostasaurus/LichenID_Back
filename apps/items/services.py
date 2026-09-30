import uuid

from fastapi import Depends, UploadFile, File

from lichenid.apps.auth.handlers import AuthHandler
from lichenid.apps.items.managers import ItemsManager



class ItemsService:
    def __init__(
            self,
            manager: ItemsManager = Depends(ItemsManager),
            handler: AuthHandler = Depends(AuthHandler)

    ) -> None:
        self.manager = manager
        self.handler = handler

    async def get_object_key(self, object_name: str, user_id: uuid.UUID | str = None) -> str:
        object_key = await self.manager.get_object_key(user_id=user_id, object_name=object_name) if user_id else object_name
        return object_key


    async def update_file(self, user_id: uuid.UUID, file: UploadFile = File(...)):
        object_key = await self.manager.get_object_key(user_id=user_id, object_name=file.filename)

        await self.manager.update_file(object_key=object_key, file=file) if object_key \
            else self.manager.upload_file(user_id=user_id, file=file)

    async def upload_file(self, user_id: uuid.UUID, file: UploadFile = File(...)):
        return await self.manager.upload_file(user_id=user_id, file=file)

