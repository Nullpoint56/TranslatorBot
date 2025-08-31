from pydantic import Field
from pydantic_extra_types.language_code import LanguageAlpha2

from model_management.base import ModelMetaBase


class BilingualModelMeta(ModelMetaBase):
    source_lang: LanguageAlpha2 = Field(..., description="Source language", examples=[LanguageAlpha2("hu")])
    target_lang: LanguageAlpha2 = Field(..., description="Target language", examples=[LanguageAlpha2("hu")])


class MultilingualModelMeta(ModelMetaBase):
    supported_languages: list[LanguageAlpha2] = Field(
        ..., description="List of supported languages", examples=[["en", "hu"]]
    )
