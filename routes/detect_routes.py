from fastapi import APIRouter
from pydantic import BaseModel
from services.ai_detector_service import detect_text_service

print('detect_routes.py loaded')
print(detect_text_service)



router = APIRouter()

class TextInput(BaseModel):
    text: str

@router.post("/")
async def detect_text(input: TextInput):
    return await detect_text_service(input.text)
