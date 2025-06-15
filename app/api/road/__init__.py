from fastapi import APIRouter, Body, Depends

from app.models.response import ApiResponse
from app.schemas.road import RoadInfo
from app.services.road import RoadServiceProtocol, get_road_service

road_router = APIRouter(prefix="/road", tags=["Road"])

@road_router.post("/sendInfo")
async def send_road_info(
    road_info: RoadInfo = Body(..., description="road_info"),
    road_service: RoadServiceProtocol = Depends(get_road_service)
):
    try:
        result = await road_service.send_road_info(road_info)
        return ApiResponse.success_response(result)
    except Exception as e:
        return ApiResponse.error_response(e)