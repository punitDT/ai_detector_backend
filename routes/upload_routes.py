from fastapi import APIRouter, UploadFile, File
from utils.file_utils import FileHandler
from services.ai_detector_service import detect_text_service
from services.document_service import DocumentService  # your class


router = APIRouter()
file_handler = FileHandler(upload_dir="uploads")
doc_service = DocumentService(upload_dir="uploads")  # ✅ create instance here

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    # 1️⃣ Save file
    file_path = await doc_service.save_upload(file)

    # 2️⃣ Extract text from file
    text = await doc_service.extract_text(file_path)

    # 3️⃣ Detect AI-generated text
    result = await detect_text_service(text)

    # 4️⃣ Delete the uploaded file
    await doc_service.delete_file(file_path)

    return result
