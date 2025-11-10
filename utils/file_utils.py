import os
from fastapi import UploadFile
import aiofiles

class FileHandler:
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)

    async def save_upload(self, file: UploadFile):
        file_path = os.path.join(self.upload_dir, file.filename)
        async with aiofiles.open(file_path, "wb") as buffer:
            while chunk := await file.read(1024):
                await buffer.write(chunk)
        return {"filename": file.filename, "path": file_path, "status": "Uploaded successfully"}
