from typing import Dict, Any

from model_management.base import ModelLoaderBase


class MarianMTModelLoader(ModelLoaderBase):

    def validate(self) -> None:
        pass

    def load(self, **kwargs) -> Dict[str, Any]:
        pass