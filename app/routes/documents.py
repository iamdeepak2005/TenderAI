# app/routes/documents.py

from fastapi import APIRouter, UploadFile,File
import os, shutil
from ..config import UPLOAD_DIR
from ..rag.document_loader import process_documents

router = APIRouter()

@router.post("/documents/upload")
async def upload_docs(files: list[UploadFile]= File(...)):
    print("✅ Upload endpoint hit")
    # Reset vector store
    shutil.rmtree("backend/vector_store", ignore_errors=True)
    os.makedirs("backend/vector_store", exist_ok=True)

    paths = []
    for file in files:
        path = os.path.join(UPLOAD_DIR, file.filename)
        with open(path, "wb") as f:
            f.write(await file.read())
        paths.append(path)

    await process_documents(paths)
    return {"message": "✅ Documents uploaded and processed."}