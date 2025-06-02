from fastapi import APIRouter

from app.models.response import ApiResponse

sys_router = APIRouter(prefix="/sys", tags=["Steam"])

@sys_router.get("/status")
def get_status():
    return ApiResponse.success_response()