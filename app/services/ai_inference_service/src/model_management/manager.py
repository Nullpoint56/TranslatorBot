from config import ModelManagerConfig


class ModelManager:
    def __init__(self, config: ModelManagerConfig):
        self.config = config

    async def translate(self, input_text: str, source_lang: str, target_lang: str) -> str:
        ...
