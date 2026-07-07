from datetime import datetime, timezone
from typing import Optional

from metronome import Metronome

from schemas.events import ImageGenerationEvent


class MetronomeClient:
    def __init__(self, bearer_token: str):
        self.client = Metronome(bearer_token=bearer_token)

    def send_image_generation_event(
        self,
        event: ImageGenerationEvent,
    ) -> None:
        self._send_usage_event(
            customer_id=event.customer_id,
            event_type=event.event_type,
            properties=event.properties,
            timestamp=event.timestamp,
            transaction_id=event.transaction_id,
        )

    def _send_usage_event(
        self,
        *,
        customer_id: str,
        event_type: str,
        properties: Optional[dict] = None,
        timestamp: datetime,
        transaction_id: str,
    ) -> None:
        payload = {
            "customer_id": customer_id,
            "event_type": event_type,
            "timestamp": self._to_rfc3339(timestamp),
            "transaction_id": transaction_id,
        }
        if properties:
            payload["properties"] = properties

        self.client.v1.usage.ingest(payload)

    def _to_rfc3339(self, dt: datetime) -> str:
        return dt.astimezone(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")