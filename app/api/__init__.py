
from fastapi import APIRouter

from app.api.sys import sys_router
from app.api.road import road_router
api_router = APIRouter()

api_router.include_router(sys_router)
api_router.include_router(road_router)

