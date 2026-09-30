from fastapi import Depends
from starlette.responses import JSONResponse

from lichenid.apps.auth.handlers import AuthHandler
from lichenid.apps.auth.schemas import UserVerifySchema
from lichenid.apps.profile.managers import ProfileManager
from lichenid.apps.profile.schemas import ChangeEmailRequest, ChangePasswordRequest


class ProfileService:
    def __init__(
            self,
            manager: ProfileManager = Depends(ProfileManager),
            handler: AuthHandler = Depends(AuthHandler)
    ) -> None:
        self.manager = manager
        self.handler = handler

    async def change_email(self, data: ChangeEmailRequest, user: UserVerifySchema) -> None | JSONResponse:
        password_hash = await self.manager.get_user_hashed_password(user_id=user.id)
        if await self.handler.verify_password(raw_password=data.password, hashed_password=password_hash):
            return await self.manager.update_user_fields(
                user_id=user.id,
                email=data.new_email)
            return None

        return JSONResponse({"error": "Invalid password"}, status_code=401)



    async def change_password(self, data: ChangePasswordRequest, user: UserVerifySchema) -> None | JSONResponse:
        current_password_hash = await self.manager.get_user_hashed_password(user_id=user.id)

        if await self.handler.verify_password(raw_password=data.old_password, hashed_password=current_password_hash):
            new_password_hash = await self.handler.get_password_hash(password=data.new_password)
            await self.manager.update_user_fields(user_id=user.id, hashed_password=new_password_hash)
            return None

        return JSONResponse({"error": "Invalid password"}, status_code=401)