from functools import lru_cache

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="_",
        extra="ignore",
    )


class MetronomeSettings(BaseModel):
    bearer_token: str = Field(
        ..., description="The bearer token for the Metronome API"
    )  # METRONOME_BEARER_TOKEN
    demo_customer_alias: str = Field(
        ..., description="The alias of the demo customer"
    )  # METRONOME_DEMO_CUSTOMER_ALIAS
    event_type: str = Field(
        ..., description="The type of event to send to the Metronome API",
        default="image_generation"
    )  # METRONOME_EVENT_TYPE


class AppSettings(Settings):
    metronome: MetronomeSettings = Field(..., description="The settings for the Metronome API")


@lru_cache
def get_app_settings() -> AppSettings:
    """
    Get the cached application settings instance.

    Constructed once and memoized via @lru_cache.
    """
    settings = AppSettings()
    return settings
