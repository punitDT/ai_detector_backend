# services/document_service.py
import os
from typing import Optional
from fastapi import UploadFile
import fitz  # PyMuPDF for PDFs
import docx

class DocumentService:
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    async def save_upload(self, file: UploadFile) -> str:
        """
        Save an uploaded file to the upload directory.
        Returns the saved file path.
        """
        file_path = os.path.join(self.upload_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return file_path

    async def delete_file(self, file_path: str):
        """
        Delete a file from the filesystem.
        """
        if os.path.exists(file_path):
            os.remove(file_path)

    async def extract_text(self, file_path: str) -> Optional[str]:
        """
        Extract text from .txt, .pdf, or .docx files.
        """
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".txt":
            return self._extract_txt(file_path)
        elif ext == ".pdf":
            return self._extract_pdf(file_path)
        elif ext == ".docx":
            return self._extract_docx(file_path)
        else:
            return None  # Unsupported file type

    def _extract_txt(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _extract_pdf(self, file_path: str) -> str:
        text = ""
        pdf_doc = fitz.open(file_path)
        for page in pdf_doc:
            text += page.get_text()
        pdf_doc.close()
        return text

    def _extract_docx(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
