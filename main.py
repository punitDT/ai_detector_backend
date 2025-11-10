from fastapi import FastAPI
from routes.detect_routes import router as detect_router
from routes.upload_routes import router as upload_router
from routes.humanize_routes import router as humanize_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="AI Text Detector API", version="2.0")

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

