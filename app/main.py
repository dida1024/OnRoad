import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import api_router
from app.core.config import settings
from app.exceptions.base import BizException
from app.core.exception_handler import biz_exception_handler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.schedulers.road import RoadScheduler

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    scheduler.add_job(RoadScheduler.send_morning_message, 'cron', hour=8, minute=30, timezone='Asia/Shanghai', id='send_morning_message')
    scheduler.add_job(RoadScheduler.send_evening_message, 'cron', hour=18, minute=30, timezone='Asia/Shanghai', id='send_evening_message')
    yield
    scheduler.shutdown()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    root_path=settings.ROOTPATH,
    lifespan=lifespan
)

# 注册异常处理器
app.add_exception_handler(BizException, biz_exception_handler)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=settings.all_cors_origins,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
