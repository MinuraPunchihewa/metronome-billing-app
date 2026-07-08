from datetime import datetime
from typing import Final, Optional

from pydantic import BaseModel


IMAGE_GENERATION_EVENT_TYPE: Final = "image_generation"


class ImageGenerationEvent(BaseModel):
    customer_id: str
    event_type: str = IMAGE_GENERATION_EVENT_TYPE
    properties: Optional[dict] = None
    timestamp: datetime
    transaction_id: str
