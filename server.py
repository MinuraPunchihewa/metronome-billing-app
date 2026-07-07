from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.router import api_router as v1_router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title="Metronome Billing API",
        description="Metronome billing API",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
        max_age=3600,
    )

    app.include_router(v1_router)

    return app


app = create_app()
