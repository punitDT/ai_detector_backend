from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ai_humanize_service import humanize_text_service

router = APIRouter()

class HumanizeRequest(BaseModel):
    text: str

@router.post("/")
async def humanize_text(request: HumanizeRequest):
    try:
        result = await humanize_text_service(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
