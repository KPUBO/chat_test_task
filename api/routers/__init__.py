from fastapi import APIRouter, Depends

from api.dependencies.deps_utils.utils import get_current_user
from api.routers.chat_router import router as chat_router
from api.routers.group_router import router as group_router
from api.routers.message_router import router as message_router
from api.routers.users_router import router as users_router


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

router.include_router(chat_router)
router.include_router(message_router)
router.include_router(group_router)
router.include_router(users_router)



