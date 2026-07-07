from typing import Final

IMAGE_GENERATION_BILLABLE_METRIC_NAME: Final = "Nova Image Generation"
IMAGE_GENERATION_BILLABLE_METRIC_GROUP_KEYS: Final[tuple[tuple[str, ...], ...]] = (("image_type",),)
IMAGE_GENERATION_BILLABLE_METRIC_AGGREGATION_KEY: Final = "num_images"