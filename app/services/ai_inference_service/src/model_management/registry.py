import os
from typing import Dict

from pydantic_extra_types.language_code import LanguageAlpha2

from model_management.config import RuntimeConfig, CTranslateModelLoaderConfig
from model_management.model import CTranslateTranslationModel


class ModelRegistry:
    _MODEL_MAP: Dict[str, tuple[LanguageAlpha2, LanguageAlpha2]] = {
        "en-hu": ("en", "hu"),
        "hu-en": ("hu", "en"),
    }
    def __init__(self):
        self.models: Dict[tuple[LanguageAlpha2, LanguageAlpha2], CTranslateTranslationModel] = {}

    def discover_and_register(self, models_root: str, runtime: RuntimeConfig = RuntimeConfig()):
        """
        Auto-discover models based on a static directory-to-language mapping.
        """
        for folder, (src, tgt) in self._MODEL_MAP.items():
            folder_path = os.path.join(models_root, folder)
            if not os.path.isdir(folder_path):
                print(f"⚠️ Skipping {folder}: directory not found")
                continue

            config = CTranslateModelLoaderConfig(
                name=folder,
                model_dir=folder_path,
                source_spm=os.path.join(folder_path, "source.spm"),
                target_spm=os.path.join(folder_path, "target.spm"),
                source_lang=src,
                target_lang=tgt,
                runtime=runtime,
            )

            model = CTranslateTranslationModel(config)
            model.load_model()
            self.models[(config.source_lang, config.target_lang)] = model

            print(f"✅ Registered model {config.source_lang} → {config.target_lang}")

    def get(self, source_lang: LanguageAlpha2, target_lang: LanguageAlpha2) -> CTranslateTranslationModel:
        key = (source_lang, target_lang)
        if key not in self.models:
            raise KeyError(f"No model for {source_lang} → {target_lang}")
        return self.models[key]
