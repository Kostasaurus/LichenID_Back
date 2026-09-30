from fastapi import  APIRouter

from lichenid.apps.auth.routes import auth_router
from lichenid.apps.profile.routes import profile_router
from lichenid.apps.items.routes import items_router


apps_router = APIRouter(
    prefix="/api/v1"
)

apps_router.include_router(router=auth_router)
apps_router.include_router(router=profile_router)
apps_router.include_router(router=items_router)