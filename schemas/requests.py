from datetime import datetime, timezone
from pydantic import BaseModel

from common.app_settings import get_app_settings
from schemas.events import ImageGenerationEvent


settings = get_app_settings()

class ImageGenerationRequest(BaseModel):
    transaction_id: str
    customer_id: str = settings.metronome.demo_customer_alias
    tier: str
    num_images: int = 1
    model: str
    region: str
    timestamp: datetime = datetime.now(timezone.utc)

    def to_event(self) -> ImageGenerationEvent:
        return ImageGenerationEvent(
            customer_id=self.customer_id,
            timestamp=self.timestamp,
            transaction_id=self.transaction_id,
            properties={
                "image_type": self.tier,
                "num_images": self.num_images,
                "model": self.model,
                "region": self.region,
            },
        )