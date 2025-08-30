import ctranslate2
import sentencepiece as spm
from pathlib import Path

class ModelManager:
    def __init__(self, models_dir: Path):
        # Load English→Hungarian
        en_hu_dir = models_dir / "en-hu"
        self.en_hu_sp = spm.SentencePieceProcessor(str(en_hu_dir / "spm.model"))
        self.en_hu_translator = ctranslate2.Translator(str(en_hu_dir), device="cpu")

        # Load Hungarian→English
        hu_en_dir = models_dir / "hu-en"
        self.hu_en_sp = spm.SentencePieceProcessor(str(hu_en_dir / "spm.model"))
        self.hu_en_translator = ctranslate2.Translator(str(hu_en_dir), device="cpu")

    def translate(self, text: str, direction: str) -> str:
        if direction == "en-hu":
            tokens = self.en_hu_sp.encode(text, out_type=str)
            results = self.en_hu_translator.translate_batch([tokens])
            output_tokens = results[0].hypotheses[0]
            return self.en_hu_sp.decode(output_tokens)

        elif direction == "hu-en":
            tokens = self.hu_en_sp.encode(text, out_type=str)
            results = self.hu_en_translator.translate_batch([tokens])
            output_tokens = results[0].hypotheses[0]
            return self.hu_en_sp.decode(output_tokens)

        else:
            raise ValueError(f"Unknown direction: {direction}")
