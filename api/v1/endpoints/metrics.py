from fastapi import APIRouter, HTTPException

from client.metronome import MetronomeClient
from schemas.requests import ImageGenerationRequest


router = APIRouter()

@router.post("/image-generation")
async def image_generation_billable_metric():
    metronome_client = MetronomeClient()

    try:
        metronome_client.create_image_generation_billable_metric()

        return {"message": "Image generation billable metric created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
