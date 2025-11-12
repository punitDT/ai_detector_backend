import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes.detect_routes import router as detect_router
from routes.upload_routes import router as upload_router
from routes.humanize_routes import router as humanize_router
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize HuggingFace Inference Client
detector_client = None
humanizer_client = None

# Model names
DETECTOR_MODEL = "openai-community/roberta-base-openai-detector"
# Using google/flan-t5-base as it's widely available on Inference API
# Note: This is a general-purpose T5 model, not specifically trained for paraphrasing
# For better paraphrasing, consider using a local model or dedicated paraphrasing service
HUMANIZER_MODEL = "google/flan-t5-base"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize HuggingFace Inference API clients on startup"""
    global detector_client, humanizer_client

    # Get HuggingFace API token from environment
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        print("⚠️  Warning: HF_TOKEN not found in environment variables")
        print("⚠️  Set HF_TOKEN to use HuggingFace Inference API")

    print("🔄 Initializing AI detector client...")
    detector_client = InferenceClient(
        provider="hf-inference",
        api_key=hf_token,
    )
    print("✅ AI detector client initialized!")

    print("� Initializing text humanizer client...")
    # Humanizer client is currently disabled - no suitable models on Inference API
    # humanizer_client = InferenceClient(
    #     provider="hf-inference",
    #     api_key=hf_token,
    # )
    print("ℹ️  Text humanizer is using placeholder implementation")

    yield

    # Cleanup (if needed)
    print("🔄 Shutting down...")

app = FastAPI(title="AI Text Detector API", version="2.0", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "https://ai-detector-app.vercel.app",
    "http://localhost:5174",
    "http://localhost:5173",
    "http://127.0.0.1:3000",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check / Test route
@app.get("/", tags=["Health"])
async def root():
    """
    Health check endpoint - returns API status and available endpoints
    """
    return {
        "status": "healthy",
        "message": "AI Text Detector API is running",
        "version": "2.0",
        "endpoints": {
            "health": "/",
            "docs": "/docs",
            "detect_text": "/api/detect",
            "upload_file": "/api/upload",
            "humanize_text": "/api/humanize"
        },
        "models": {
            "detector": DETECTOR_MODEL,
            "humanizer": HUMANIZER_MODEL + " (placeholder)"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Simple health check endpoint for monitoring
    """
    return {"status": "ok"}

# Include route files
app.include_router(detect_router, prefix="/api/detect", tags=["Detection"])
app.include_router(upload_router, prefix="/api/upload", tags=["Upload"])
app.include_router(humanize_router, prefix="/api/humanize", tags=["Humanizer"])

if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", 8000))  # default for local
    uvicorn.run("main:app", host="0.0.0.0", port=port)


