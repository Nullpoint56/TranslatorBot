from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Dict, Any
from typing import Optional

from pydantic import BaseModel, Field


class QuantizationType(Enum):
    INT8 = "int8"
    FP16 = "fp16"
    FP32 = "fp32"


class ModelLoaderBase(ABC):
    def __init__(self, model_dir: Path):
        self.model_dir = model_dir

    @abstractmethod
    def validate(self) -> None:
        ...

    @abstractmethod
    def load(self, **kwargs) -> Dict[str, Any]:
        """Load and return artifacts + metadata"""
        ...


class ModelMetaBase(BaseModel):
    id: str = Field(..., description="Internal model identifier", examples=["opus-mt-en-hu-int8"])
    name: Optional[str] = Field(None, description="Human-readable name", examples=["EN->HU MarianMT Int8"])
    multilanguage: bool = Field(False, description="If the model supports multiple languages", examples=[False])
    description: Optional[str] = Field(None, description="Model description",
                                       examples=["MarianMT model capable of ..."])
    quantization: Optional[QuantizationType] = Field(None, description="Quantization type",
                                                     examples=[QuantizationType.INT8])
    vocab_size: Optional[int] = Field(None, description="Model vocabulary size", examples=[2048])
    model_max_input_length: Optional[int] = Field(None, description="Model max input length", examples=[1024])
    model_max_output_length: Optional[int] = Field(None, description="Model max output length", examples=[512])
