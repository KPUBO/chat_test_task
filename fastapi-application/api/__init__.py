from fastapi import APIRouter
from api.api_v1 import router as api_v1_router


router = APIRouter()
router.include_router(api_v1_router)
