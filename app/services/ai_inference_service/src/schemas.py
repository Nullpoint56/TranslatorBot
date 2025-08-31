from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints
from pydantic_extra_types.language_code import LanguageAlpha2


class TranslationRequest(BaseModel):
    text: Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=256)] = Field(
        ..., description="Text to translate"
    )
    source_lang: LanguageAlpha2 = Field(..., description="Translation source language")
    target_lang: LanguageAlpha2 = Field(..., description="Translation target language")

    class Config:
        json_schema_extra = {
            "example": {"text": "Hello world", "source_lang": "en", "target_lang": "hu"}
        }


class TranslationResponse(BaseModel):
    translation: Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=256)] = Field(
        ..., description="Translated text"
    )

    class Config:
        json_schema_extra = {
            "example": {"translation": "Helló világ"}
        }
