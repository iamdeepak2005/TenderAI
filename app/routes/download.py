from fastapi import APIRouter, HTTPException
from ..rag.document_loader import process_documents
from ..rag.query_engine import ask_detail
import os
import requests
from tempfile import NamedTemporaryFile

router = APIRouter()

@router.post("/download-and-summarize/")
async def download_and_summarize(url: str):
    try:
        # Download the file
        response = requests.get(url)
        response.raise_for_status()

        # Create a temporary file to save the content
        with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(response.content)
            tmp_file_path = tmp_file.name

        # Load the document
        documents = await process_documents([tmp_file_path])

        # Summarize the document (assuming summarize_document takes a list of documents)
        summary = ask_detail("Give me the detailed explaniation..")

        # Clean up the temporary file
        os.unlink(tmp_file_path)

        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
