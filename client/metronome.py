from datetime import datetime, timezone
from typing import Dict, List, Optional

from metronome import Metronome

from common.app_settings import get_app_settings


settings = get_app_settings()

class MetronomeClient:
    def __init__(self, bearer_token: str = settings.metronome.bearer_token):
        self.client = Metronome(bearer_token=bearer_token)

    def send_usage_event(
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

    def create_billable_metric(
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

    def list_billable_metrics(self) -> List[Dict]:
        response = self.client.v1.billable_metrics.list()
        return [metric.model_dump() for metric in getattr(response, "data", [])]
    
    def create_product(
        self,
        *,
        name: str,
        billable_metric_id: str,
        pricing_group_key: Optional[List[str]] = None,
        presentation_group_key: Optional[List[str]] = None,
    ) -> Dict:
        payload = {
            "name": name,
            "type": "USAGE",
            "billable_metric_id": billable_metric_id,
        }
        if pricing_group_key:
            payload["pricing_group_key"] = pricing_group_key
        if presentation_group_key:
            payload["presentation_group_key"] = presentation_group_key
        response = self.client.v1.contracts.products.create(**payload)
        return response.data.model_dump() if hasattr(response, "data") else {}

    def create_rate_card(
        self,
        *,
        name: str,
        description: str = "",
    ) -> Dict:
        response = self.client.v1.contracts.rate_cards.create(
            name=name,
            description=description or f"Pricing for {name}",
        )
        return response.data.model_dump() if hasattr(response, "data") else {}

    def add_flat_rate(
        self,
        *,
        rate_card_id: str,
        product_id: str,
        price_cents: int,
        starting_at: str,
        pricing_group_values: Optional[Dict[str, str]] = None,
    ) -> Dict:
        payload = {
            "rate_card_id": rate_card_id,
            "product_id": product_id,
            "entitled": True,
            "rate_type": "FLAT",
            "price_cents": price_cents,
            "starting_at": starting_at,
        }
        if pricing_group_values:
            payload["pricing_group_values"] = pricing_group_values
        response = self.client.v1.contracts.rate_cards.rates.add(**payload)
        return response.data.model_dump() if hasattr(response, "data") else {}