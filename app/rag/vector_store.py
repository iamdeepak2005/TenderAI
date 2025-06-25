# app/rag/vector_store.py

from langchain_chroma import Chroma
from ..config import CHROMA_PATH
import os
import asyncio


os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"

# def save_to_vectordb(chunks, embeddings):
#     print("📦 Creating new Chroma vector store (no persistence)...")
#     try:
#         vectordb = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)
#         print("✅ Vector store created (in-memory only)")
#         vectordb.persist()  # Save to disk
#     except Exception as e:
#         print("❌ Error during in-memory vector store creation:", str(e))

def get_vectordb(embedding_model):
    print("🔄 Loading Chroma vector store from:", CHROMA_PATH)
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_model
    )


async def save_to_vectordb(chunks, embeddings):
    print("📦 Creating new Chroma vector store (async)...")

    vectordb = await asyncio.to_thread(
        Chroma.from_documents,
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    await asyncio.to_thread(vectordb.persist)
    print("✅ Vector store saved to:", CHROMA_PATH)

