# app/rag/document_loader.py

import pdfplumber
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from ..config import CHROMA_PATH
from .vector_store import save_to_vectordb
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"

RAW_TEXTS = []

async def process_documents(filepaths):
    global RAW_TEXTS
    RAW_TEXTS.clear()
    docs = []

    print("📥 Files received:", filepaths)

    for path in filepaths:
        print(f"📄 Reading: {path}")
        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text:
                    text = ""
                table_data = page.extract_tables()
                if table_data:
                    for table in table_data:
                        table_str = "\n".join(
                            ["\t".join(cell if cell is not None else "" for cell in row) for row in table if row]
                        )
                        text += "\n\n📊 Extracted Table:\n" + table_str
                if text.strip():
                    print(f"📝 Page {i + 1} has text of length {len(text)}")
                    docs.append(Document(page_content=text, metadata={"source": path, "page": i + 1}))
                    RAW_TEXTS.append(text)
                print(text[:1000])
    # splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    # chunks = splitter.split_documents(docs)
    # print(f"✂️ Split into {len(chunks)} chunks")

    # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    # print("🧠 Embeddings initialized")

    # await save_to_vectordb(chunks, embeddings)
    # print("✅ Saved to vector store")

    # print(f"✅ Processed {len(docs)} pages from {len(filepaths)} file(s).")
