from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from lichenid.apps.auth.schemas import UserVerifySchema
from lichenid.apps.profile.schemas import ChangeEmailRequest, ChangePasswordRequest
from lichenid.apps.auth.depends import get_current_user
from lichenid.apps.profile.services import ProfileService

profile_router = APIRouter(prefix="/profile", tags=["profile"])

@profile_router.post(
    path="/change-email",
    status_code=status.HTTP_200_OK
)
async def change_email(
        data: ChangeEmailRequest,
        user: Annotated[UserVerifySchema, Depends(get_current_user)],
        service: ProfileService = Depends(ProfileService)
):
    return await service.change_email(data=data, user=user)

@profile_router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
)
async def change_password(
    data: ChangePasswordRequest,
    user: Annotated[UserVerifySchema, Depends(get_current_user)],
    service: ProfileService = Depends(ProfileService),
) -> Response:
    return await service.change_password(data=data, user=user)


