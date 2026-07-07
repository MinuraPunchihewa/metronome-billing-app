from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ImageGenerationEvent(BaseModel):
    customer_id: str
    event_type: str
    properties: Optional[dict] = None
    timestamp: datetime
    transaction_id: str