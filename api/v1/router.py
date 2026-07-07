from fastapi import APIRouter

from api.v1.endpoints.events import router as events_router
from api.v1.endpoints.metrics import router as metrics_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(events_router, prefix="/events", tags=["events"])
api_router.include_router(metrics_router, prefix="/metrics", tags=["metrics"])