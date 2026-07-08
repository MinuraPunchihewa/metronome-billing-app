from client.metronome import MetronomeClient
from schemas.events import IMAGE_GENERATION_EVENT_TYPE
from provisioning.metrics import (
    IMAGE_GENERATION_BILLABLE_METRIC_AGGREGATION_KEY,
    IMAGE_GENERATION_BILLABLE_METRIC_GROUP_KEYS,
    IMAGE_GENERATION_BILLABLE_METRIC_NAME,
)
from provisioning.rates import (
    IMAGE_GENERATION_BILLABLE_PRICES,
    IMAGE_GENERATION_PRODUCT_NAME,
    IMAGE_GENERATION_RATE_CARD_NAME,
    IMAGE_GENERATION_RATE_EFFECTIVE_AT,
)


def main() -> None:
    metronome_client = MetronomeClient()

    # Billable Metric
    billable_metric = metronome_client.create_billable_metric(
        name=IMAGE_GENERATION_BILLABLE_METRIC_NAME,
        event_type=IMAGE_GENERATION_EVENT_TYPE,
        aggregation_key=IMAGE_GENERATION_BILLABLE_METRIC_AGGREGATION_KEY,
        group_keys=IMAGE_GENERATION_BILLABLE_METRIC_GROUP_KEYS,
        property_filters=[
            {"name": "image_type", "exists": True},
            {"name": "num_images", "exists": True},
        ]
    )
    print(f"Created billable metric {IMAGE_GENERATION_BILLABLE_METRIC_NAME}.")

    # Product
    pricing_group_keys = [key[0] for key in IMAGE_GENERATION_BILLABLE_METRIC_GROUP_KEYS]
    product = metronome_client.create_product(
        name=IMAGE_GENERATION_PRODUCT_NAME,
        billable_metric_id=billable_metric["id"],
        pricing_group_key=pricing_group_keys,
        presentation_group_key=pricing_group_keys,
    )
    print(f"Created product {IMAGE_GENERATION_PRODUCT_NAME}.")

    # Rate Card
    rate_card = metronome_client.create_rate_card(
        name=IMAGE_GENERATION_RATE_CARD_NAME,
    )
    print(f"Created rate card {IMAGE_GENERATION_RATE_CARD_NAME}.")

    # Flat Rate
    rates = {}
    for image_type, price in IMAGE_GENERATION_BILLABLE_PRICES.items():
        rate = metronome_client.add_flat_rate(
            rate_card_id=rate_card["id"],
            product_id=product["id"],
            price_cents=int(price),
            starting_at=IMAGE_GENERATION_RATE_EFFECTIVE_AT,
            pricing_group_values={
                "image_type": image_type,
            },
        )
        rid = rate.get("id") or rate.get("rate_id")
        rates[image_type] = {"id": rid, "price_cents": int(price)}
        print(f"Added flat rate for {image_type}.")

    print("Metronome provisioning complete.")


if __name__ == "__main__":
    main()
