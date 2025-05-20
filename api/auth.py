from fastapi import APIRouter

from api.dependencies.authentication.backend import authentication_backend
from api.dependencies.authentication.fastapi_users import fastapi_users
from core.schemas.user import UserRead, UserCreate, UserUpdate

router = APIRouter(prefix='/auth/jwt', tags=["Auth"])
router.include_router(
    fastapi_users.get_auth_router(authentication_backend, requires_verification=True),
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
)

router.include_router(
    fastapi_users.get_reset_password_router(),
)

router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate))
