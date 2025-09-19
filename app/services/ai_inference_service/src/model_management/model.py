import ctranslate2
import sentencepiece as spm
from .config import CTranslateModelLoaderConfig


class CTranslateTranslationModel:
    def __init__(self, config: CTranslateModelLoaderConfig):
        self.config = config
        self.translator = None
        self.sp_source = None
        self.sp_target = None

    def load_model(self):
        kwargs = self.config.runtime.model_dump()
        self.translator = ctranslate2.Translator(self.config.model_dir, **kwargs)
        self.sp_source = spm.SentencePieceProcessor().Init(model_file=self.config.source_spm)
        self.sp_target = spm.SentencePieceProcessor().Init(model_file=self.config.target_spm)

    def translate(self, text: str, beam_size: int | None = None) -> str:
        """Run translation using the loaded model."""
        if not self.translator or not self.sp_source or not self.sp_target:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        tokens = self.sp_source.encode(text, out_type=str)
        results = self.translator.translate_batch(
            [tokens],
            beam_size=beam_size or self.config.runtime.beam_size,
        )
        return self.sp_target.decode(results[0].hypotheses[0])
