from fastapi import FastAPI
from routes.detect_routes import router as detect_router
from routes.upload_routes import router as upload_router
from routes.humanize_routes import router as humanize_router
from fastapi.middleware.cors import CORSMiddleware
import nltk
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForSeq2SeqLM, pipeline
import torch

app = FastAPI(title="AI Text Detector API", version="2.0")

# Preload model at startup
@app.on_event("startup")
def load_model():
    # Ensure tokenizers are downloaded
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download("punkt", quiet=True)

    MODEL_NAME = "openai-community/roberta-base-openai-detector"
    HUMANIZE_MODEL_NAME = "rVamsi/T5_Paraphrase_Paws"
    print("🔄 Loading AI detector model...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    detector = pipeline("text-classification", model=model, tokenizer=tokenizer, truncation=True)

    print("✅ Model loaded successfully!")

    HUMANIZE_MODEL_NAME = "pszemraj/flan-t5-base-instruct-dolly_hhrlhf"

    print("🔄 Loading Text Humanizer model...")

    # Load model and tokenizer once globally
    humanizeTokenizer = AutoTokenizer.from_pretrained(HUMANIZE_MODEL_NAME)
    humanizeModel = AutoModelForSeq2SeqLM.from_pretrained(HUMANIZE_MODEL_NAME)

    # Move to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    humanizeModel = humanizeModel.to(device)

    print("✅ Humanizer model loaded successfully!")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5174",
    "http://localhost:5173",
    "http://127.0.0.1:3000",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include route files
app.include_router(detect_router, prefix="/api/detect", tags=["Detection"])
app.include_router(upload_router, prefix="/api/upload", tags=["Upload"])
app.include_router(humanize_router, prefix="/api/humanize", tags=["Humanizer"])

if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", 8000))  # default for local
    uvicorn.run("main:app", host="0.0.0.0", port=port)


