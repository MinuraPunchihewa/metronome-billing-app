from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from client.events import IMAGE_GENERATION_EVENT_TYPE


class ImageGenerationEvent(BaseModel):
    customer_id: str
    event_type: str = IMAGE_GENERATION_EVENT_TYPE
    properties: Optional[dict] = None
    timestamp: datetime
    transaction_id: str