from datetime import datetime, timezone
from typing import Dict, List, Optional

from metronome import Metronome

from common.app_settings import get_app_settings
from client.events import IMAGE_GENERATION_EVENT_TYPE
from client.metrics import (
    IMAGE_GENERATION_BILLABLE_METRIC_NAME,
    IMAGE_GENERATION_BILLABLE_METRIC_GROUP_KEYS,
    IMAGE_GENERATION_BILLABLE_METRIC_AGGREGATION_KEY,
)
from schemas.events import ImageGenerationEvent


settings = get_app_settings()

class MetronomeClient:
    def __init__(self, bearer_token: str = settings.metronome.bearer_token):
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

        self.client.v1.usage.ingest(usage=[payload])

    def _to_rfc3339(self, dt: datetime) -> str:
        return dt.astimezone(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")

    def create_image_generation_billable_metric(self) -> None:
        self._create_billable_metric(
            name=IMAGE_GENERATION_BILLABLE_METRIC_NAME,
            event_type=IMAGE_GENERATION_EVENT_TYPE,
            aggregation_key=IMAGE_GENERATION_BILLABLE_METRIC_AGGREGATION_KEY,
            group_keys=IMAGE_GENERATION_BILLABLE_METRIC_GROUP_KEYS,
            property_filters=[
                {"name": "image_type", "exists": True},
                {"name": "num_images", "exists": True},
            ]
        )

    def _create_billable_metric(
        self,
        *,
        name: str,
        event_type: str,
        aggregation_type: str = "SUM",
        aggregation_key: Optional[str] = None,
        group_keys: Optional[List[List[str]]] = None,
        property_filters: Optional[List[Dict]] = None,
    ) -> None:
        params = {
            "name": name,
            "aggregation_type": aggregation_type,
            "event_type_filter": {"in_values": [event_type]},
        }
        if aggregation_key:
            params["aggregation_key"] = aggregation_key
        if group_keys:
            params["group_keys"] = [list(keys) for keys in group_keys]
        if property_filters:
            params["property_filters"] = property_filters

        response = self.client.v1.billable_metrics.create(**params)
        return response.data.model_dump() if hasattr(response, "data") else {}