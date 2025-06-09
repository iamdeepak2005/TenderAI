from pypdf import PdfReader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from deepseek_client import query_llm
import re
from typing import List, Dict
from langchain_community.embeddings import SentenceTransformerEmbeddings

SECTION_EXTRACTION_PROMPT = """
You are given the full content of a document below.

Identify the main **sections** in this document based on content. 
Return a list of section **titles** only — no summaries, just titles. 
Ignore repeated headers like page numbers or footers.

Document:
{content}

List the section titles:
"""

# Prompts
SUMMARY_PROMPT = """You are an expert summarizer. Read the following tender content and give a detailed executive summary.

Text:
{text}

Summary:"""

DETAIL_SECTION_PROMPT = """Analyze the following section titled '{title}'.

Section Content:
{content}

Based on this, provide insights and elaborate if relevant to:
'{question}'
"""

GENERAL_PROMPT = """You are a tender assistant. Answer based only on the context below.

Context:
{context}

Question: {question}

Answer:"""

CHROMA_PATH = "backend/vector_store"

# Global store for raw texts (for summary and detail section extraction)
RAW_TEXTS: List[str] = []

# Keywords to classify questions
SUMMARY_KEYWORDS = ["summary", "overview", "brief", "highlights"]
DETAIL_KEYWORDS = ["explain", "elaborate", "details", "section", "clause", "content", "in-depth"]

# ------------------------
# 📄 Load & Process Documents
# ------------------------
def process_documents(filepaths: List[str]):
    global RAW_TEXTS
    RAW_TEXTS = []

    docs = []
    for path in filepaths:
        reader = PdfReader(path)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            if text:  # Make sure text is not None
                docs.append(Document(
                    page_content=text,
                    metadata={"source": path, "page": page_num + 1}
                ))
                RAW_TEXTS.append(text)

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    # Use free HuggingFace embeddings
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)
    vectordb.persist()


# -------------------------------
# 🤖 Query Classification Helpers
# -------------------------------
def is_summary_question(question: str) -> bool:
    return any(word in question.lower() for word in SUMMARY_KEYWORDS)

def is_detail_question(question: str) -> bool:
    return any(word in question.lower() for word in DETAIL_KEYWORDS)

# -------------------------
# 🤖 Main Query Handler
# -------------------------
def query_rag(question: str) -> str:
    if is_summary_question(question):
        return ask_summary(question)
    elif is_detail_question(question):
        return ask_detail(question)
    else:
        return ask_general(question)

# ----------------------
# ✨ General Query Flow
# ----------------------
def ask_summary(question: str) -> str:
    full_text = "\n".join(RAW_TEXTS)
    cleaned_text = preprocess_text(full_text)
    prompt = SUMMARY_PROMPT.format(text=cleaned_text)
    return query_llm(prompt)

def ask_detail(question: str):
    sections = extract_sections_via_llm(RAW_TEXTS)
    
    # 1. 🔹 Show available sections first
    yield "## 📄 Available Sections:\n"
    for title in sections.keys():
        yield f"- {title}\n"
    yield "\n---\n\n"

    # 2. 🔹 Then process each section one by one
    for title, content in sections.items():
        prompt = DETAIL_SECTION_PROMPT.format(title=title, content=content, question=question)
        answer = query_llm(prompt)  # Replace with async if needed
        yield f"### 🔍 Section: {title} ###\n{answer.strip()}\n\n"


def ask_general(question: str) -> str:
    vectordb = Chroma(persist_directory=CHROMA_PATH, embedding_function=OpenAIEmbeddings())
    results = vectordb.similarity_search(question, k=3)
    context = "\n".join([doc.page_content for doc in results])
    prompt = GENERAL_PROMPT.format(context=context, question=question)
    return query_llm(prompt)

# --------------------------
# 🧹 Text Preprocessing
# --------------------------
def preprocess_text(text: str) -> str:
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)
    # Remove unwanted characters (keep alphanumerics and common punctuation)
    text = re.sub(r"[^A-Za-z0-9,.:%() \n\-]", "", text)
    return text.strip()

# --------------------------
# 🔎 Extract Document Sections
# --------------------------
def extract_sections_via_llm(raw_texts: List[str]) -> Dict[str, str]:
    full_text = "\n".join(raw_texts)
    
    # Step 1: Ask the LLM what sections exist
    prompt = SECTION_EXTRACTION_PROMPT.format(content=full_text[:3000])  # limit to avoid token overload
    section_titles_raw = query_llm(prompt)
    
    # Step 2: Extract and split titles from response
    section_titles = [line.strip("-•* \n") for line in section_titles_raw.strip().split("\n") if line.strip()]

    # Step 3: Match content under each section
    sections = {}
    for title in section_titles:
        # Find title in text and extract everything until the next one
        match = re.search(re.escape(title), full_text, re.IGNORECASE)
        if not match:
            continue
        start = match.start()
        end = None
        for next_title in section_titles:
            if next_title == title:
                continue
            m = re.search(re.escape(next_title), full_text[start + 1:], re.IGNORECASE)
            if m:
                end = start + 1 + m.start()
                break
        content = full_text[start:end].strip() if end else full_text[start:].strip()
        sections[title] = content

    return sections

