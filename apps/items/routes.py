from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File
from starlette import status
from starlette.responses import Response, JSONResponse

from lichenid.apps.auth.schemas import UserVerifySchema
from lichenid.apps.auth.depends import get_current_user
from lichenid.apps.items.services import ItemsService

items_router = APIRouter(prefix="/items", tags=["items"])


@items_router.get(
    "/get-collection",
    status_code=status.HTTP_200_OK
)
async def get_collection(
        user: Annotated[UserVerifySchema, Depends(get_current_user)],
        service: ItemsService = Depends(ItemsService)
) -> str:
    return await service.get_object_key(user_id=user.id, object_name="collection")


@items_router.post(
    "/update-collection",
    status_code=status.HTTP_200_OK
)
async def change_collection(
    file: UploadFile,
    user: Annotated[UserVerifySchema, Depends(get_current_user)],
    service: ItemsService = Depends(ItemsService)
):
    return await service.update_file(user_id=user.id, file=file)

@items_router.post("/upload-photo")
async def upload_photo(
    photo: UploadFile,
    user: Annotated[UserVerifySchema, Depends(get_current_user)],
    service: ItemsService = Depends(ItemsService)
):
    return await service.upload_file(user_id=user.id, file=photo)

@items_router.get("/get-key/{object_name}")
async def get_object_key(
        object_name: str,
        user: Annotated[UserVerifySchema, Depends(get_current_user)],
        service: ItemsService = Depends(ItemsService)
):
    return await service.get_object_key(object_name=object_name, user_id=user.id)
