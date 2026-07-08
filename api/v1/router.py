from fastapi import APIRouter

from api.v1.endpoints.events import router as events_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(events_router, prefix="/events", tags=["events"])