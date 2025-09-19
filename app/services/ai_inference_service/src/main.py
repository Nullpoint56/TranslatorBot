from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic_extra_types.language_code import LanguageAlpha2

from model_management.registry import ModelRegistry
from schemas import TranslationRequest, TranslationResponse


async def run_translation(app: FastAPI, text: str, source: LanguageAlpha2, target: LanguageAlpha2,
                          beam_size: int | None = None) -> str:
    registry: ModelRegistry = app.state.model_registry
    try:
        model = registry.get(source, target)
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Unsupported language pair: {source}-{target}")

    return model.translate(text, beam_size=beam_size)


@asynccontextmanager
async def lifespan(app: FastAPI):
    registry = ModelRegistry()
    registry.discover_and_register("models")
    app.state.model_registry = registry
    print("✅ Models loaded into memory")
    yield
    app.state.model_registry = None


app = FastAPI(title="AI Inference Service", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/translate", response_model=TranslationResponse)
async def translate(req: TranslationRequest):
    try:
        output = await run_translation(app, req.text, req.source_lang, req.target_lang, req.beam_size)
        return TranslationResponse(translation=output)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
