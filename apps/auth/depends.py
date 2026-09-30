import uuid

from fastapi import HTTPException
from typing import Annotated
from starlette import  status

from fastapi import Depends

from lichenid.apps.auth.handlers import AuthHandler
from lichenid.apps.auth.managers import UserManager
from lichenid.apps.auth.schemas import UserVerifySchema
from lichenid.apps.auth.utils import get_token_from_cookies


async def get_current_user(
        token: Annotated[str, Depends(get_token_from_cookies)],
        handler: AuthHandler = Depends(AuthHandler),
        manager: UserManager = Depends(UserManager)
) -> UserVerifySchema:
    decoded_token = await handler.decode_access_token(token)

    user_id = decoded_token.get("user_id")
    session_id = decoded_token.get("session_id")

    if not await manager.get_access_token(user_id=user_id, session_id=session_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await manager.get_user_by_id(user_id=uuid.UUID(user_id))

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    user.session_id = session_id

    return user