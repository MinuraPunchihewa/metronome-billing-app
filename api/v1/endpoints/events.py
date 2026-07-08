from fastapi import APIRouter, HTTPException

from client.metronome import MetronomeClient
from schemas.requests import ImageGenerationRequest


router = APIRouter()

@router.post("/image-generation")
async def image_generation(request: ImageGenerationRequest):
    metronome_client = MetronomeClient()
    event = request.to_event()

    try:
        metronome_client.send_usage_event(
            customer_id=event.customer_id,
            event_type=event.event_type,
            properties=event.properties,
            timestamp=event.timestamp,
            transaction_id=event.transaction_id,
        )

        return {"message": "Image generation event sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
