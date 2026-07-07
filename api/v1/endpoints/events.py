from fastapi import APIRouter, HTTPException

from client.metronome import MetronomeClient
from schemas.requests import ImageGenerationRequest


router = APIRouter()

@router.post("/image-generation")
async def image_generation(request: ImageGenerationRequest):
    metronome_client = MetronomeClient()

    try:
        metronome_client.send_image_generation_event(request.to_event())

        return {"message": "Image generation event sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
