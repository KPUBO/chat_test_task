from fastapi import APIRouter
from core.config import settings
from api.router.users_router import router as users_router

router = APIRouter(
    prefix=settings.api.v1.prefix
)

router.include_router(users_router)
