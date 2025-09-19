from pydantic import BaseModel, Field
from typing import Literal

from pydantic_extra_types.language_code import LanguageAlpha2


class RuntimeConfig(BaseModel):
    """Runtime tuning options for CTranslate2 models."""

    device: Literal["cpu", "cuda", "auto"] = Field(
        default="cpu", description="Device for inference"
    )
    device_index: int = Field(
        default=0, description="Device index (e.g., GPU id or CPU id)"
    )
    inter_threads: int = Field(
        default=1, description="Number of independent CPU workers"
    )
    intra_threads: int = Field(
        default=1, description="Threads per CPU worker"
    )
    num_workers: int = Field(
        default=1, description="Number of translator replicas"
    )
    max_queued_batches: int = Field(
        default=1, description="Maximum number of queued batches"
    )
    compute_type: Literal["default", "int8", "int16", "float16", "bfloat16"] = Field(
        default="default", description="Computation type for optimized inference"
    )
    beam_size: int = Field(default=4, description="Default beam size for translation")


class CTranslateModelLoaderConfig(BaseModel):
    """Configuration for loading a CTranslate2 model + tokenizers."""

    name: str = Field(..., description="Unique model identifier (e.g., 'en-hu')")
    model_dir: str = Field(..., description="Path to the CTranslate2 model directory")
    source_spm: str = Field(..., description="Path to SentencePiece source tokenizer")
    target_spm: str = Field(..., description="Path to SentencePiece target tokenizer")
    source_lang: LanguageAlpha2 = Field(..., description="Source language code (e.g., 'en')")
    target_lang: LanguageAlpha2 = Field(..., description="Target language code (e.g., 'hu')")

    runtime: RuntimeConfig = Field(
        default_factory=RuntimeConfig,
        description="Runtime parallelism and optimization settings",
    )
