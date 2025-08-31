from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException

from config import ModelManagerConfig
from model_management.manager import ModelManager
from schemas import TranslationRequest, TranslationResponse

# Global reference (set at startup)
model_manager: ModelManager | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_manager
    model_manager = ModelManager(
        ModelManagerConfig(
            model_dir=Path()
        )
    )
    print("✅ Models loaded into memory")
    yield
    model_manager = None
    print("🛑 Models released")


app = FastAPI(title="AI Inference Service", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/translate", response_model=TranslationResponse)
async def translate(req: TranslationRequest):
    try:
        output = await model_manager.translate(req.text, req.source_lang, req.target_lang)
        return TranslationResponse(translation=output)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
