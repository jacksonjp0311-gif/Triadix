from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    run_root: str = str(Path.cwd() / "triadix-run")
    blocks: int = 96
    tau: float = 0.244
    health_mode: str = "p25"
    health_min_fraction: float = 0.95
    min_health_blocks: int = 12

    model_config = SettingsConfigDict(
        env_prefix="TRIADIX_",
        env_file=".env"
    )


def get_config() -> Settings:
    return Settings()