import os
import shutil
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

# ✅ Step 1: Load and split PDF documents
def load_and_split_docs(folder="documents"):
    all_docs = []
    print(os.getcwd())
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(folder, file))
            all_docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(all_docs)

# ✅ Step 2: Create and persist vector store
def create_vectorstore(docs, persist_dir="db"):
    embedder = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(docs, embedding=embedder, persist_directory=persist_dir)
    vectordb.persist()
    return vectordb

# ✅ Step 3: Build the RAG chain
def build_chat_rag(force_refresh=False):
    persist_dir = "db"

    if force_refresh and os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)

    if not os.path.exists(persist_dir) or not os.listdir(persist_dir):
        docs = load_and_split_docs()
        vectordb = create_vectorstore(docs)
    else:
        embedder = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        vectordb = Chroma(persist_directory=persist_dir, embedding_function=embedder)

    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    OPENROUTER_API_KEY = "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"  # 🔐 Replace this!

    llm = ChatOpenAI(
        model_name="meta-llama/llama-3-8b-instruct",
        temperature=0.7,
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key=OPENROUTER_API_KEY,
    )

    rag_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
    )

    return rag_chain

# ✅ Step 4: Main execution
def main():
    print("📂 Make sure PDF files are in the 'documents' folder.")
    force_refresh = input("❓ Rebuild vector DB from scratch? (y/n): ").strip().lower() == "y"

    chat_rag = build_chat_rag(force_refresh=force_refresh)

    print("\n💬 Chat with your PDF! Type 'exit' to quit.\n")

    while True:
        query = input("👤 You: ")
        if query.lower() in ["exit", "quit"]:
            print("👋 Chat ended.")
            break
        response = chat_rag.run({"question": query, "chat_history": []})
        print(f"🤖 {response}\n")


if __name__ == "__main__":
    main()
