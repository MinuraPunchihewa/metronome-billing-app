from functools import lru_cache

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


class MetronomeSettings(BaseModel):
    bearer_token: str = Field(
        ..., description="The bearer token for the Metronome API"
    )  # METRONOME_BEARER_TOKEN
    demo_customer_alias: str = Field(
        ..., description="The alias of the demo customer"
    )  # METRONOME_DEMO_CUSTOMER_ALIAS


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
