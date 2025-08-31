from pathlib import Path

from pydantic import BaseModel, model_validator


class AppConfig(BaseModel):
    log_level: str
    log_dir: Path


class ModelManagerConfig(BaseModel):
    model_dir: Path

    @model_validator(mode="after")
    def check_models_dir(cls, values):
        if not values.models_dir.exists():
            raise ValueError(f"Models dir does not exist: {values.models_dir}")
        if not values.models_dir.is_dir():
            raise ValueError(f"Models dir is not a directory: {values.models_dir}")
        return values
