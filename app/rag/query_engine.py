import os
from langchain.prompts import PromptTemplate
from app.agents.agent_initializer import get_llm
from .query_classifier import is_summary_question, is_detail_question
from .vector_store import get_vectordb
from langchain.chains import  RetrievalQA
from langchain.chains.llm import LLMChain
from langchain_huggingface import HuggingFaceEmbeddings
from ..prompts.general_prompt import GENERAL_PROMPT
from ..prompts.summary_prompt import SUMMARY_PROMPT
from ..prompts.section_prompt import DETAIL_SECTION_PROMPT
from ..prompts.extract_titles import DETAILED_TENDER_ANALYSIS_PROMPT
from ..prompts.summary_prompt_pdf import SUMMARY_PROMPT_PDF
from ..prompts.section_prompt_pdf import DETAIL_SECTION_PROMPT_PDF


os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
# Initialize embedding model once
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
llm = get_llm()
# def extract_section_titles():
#     full_text = "\n".join(get_raw_texts())
#     prompt = SECTION_EXTRACTION_PROMPT.format(content=full_text)
#     response = llm.invoke(prompt).content
#     titles = [line.strip("- ").strip() for line in response.strip().splitlines() if line.startswith("-")]
#     return titles

def ask_summary(question: str) -> str:
    text = "\n".join(get_raw_texts())
    prompt = SUMMARY_PROMPT.format(text=text)
    
    return llm.invoke(prompt).content

def ask_summary_pdf(question: str) -> str:
    text = "\n".join(get_raw_texts())
    prompt = SUMMARY_PROMPT_PDF.format(text=text)
    return llm.invoke(prompt).content
# def ask_detail(question: str):
#     print(f"\n⚡ ask_detail called with question: {question}")
#     full_text = "\n".join(get_raw_texts())
#     section_titles = extract_section_titles()
#     print(f"🔍 Extracted section titles: {section_titles}")
#     for title in section_titles:
#             prompt = DETAIL_SECTION_PROMPT.format(
#                 title=title,
#                 content=full_text,
#                 question=question
#             )
#             response = llm.invoke(prompt).content
#             print(response)
#             yield f"## 📌 {title}\n{response.strip()}\n"
def ask_detail(question: str):
        text = "\n".join(get_raw_texts())
        prompt = DETAILED_TENDER_ANALYSIS_PROMPT.format(text=text)
        return llm.invoke(prompt).content



# def ask_detail_pdf(question: str) -> str:
#     print(f"\n⚡ ask_detail called with question: {question}")
    
#     full_text = "\n".join(get_raw_texts())
#     section_titles = extract_section_titles()
#     print(f"🔍 Extracted section titles: {section_titles}")
    
#     detailed_sections = []

#     for title in section_titles:
#         prompt = DETAIL_SECTION_PROMPT_PDF.format(
#             title=title,
#             content=full_text,
#             question=question
#         )
#         response = llm.invoke(prompt).content
#         print(response)
#         detailed_sections.append(f"## 📌 {title}\n{response.strip()}\n")

#     return "\n\n".join(detailed_sections)


# def ask_general(question: str) -> str:
#     print(f"\n⚡ ask_general called with question: {question}")
#     try:
#         # Step 1: Load vector DB
#         vectordb = get_vectordb(embedding_model)
#         print(f"✅ Vector DB initialized: {vectordb}")

#         # Step 2: Create retriever
#         retriever = vectordb.as_retriever(search_kwargs={"k": 4})
#         print(f"🔍 Retriever created: {retriever}")

#         # Step 3: Create prompt template
#         prompt = PromptTemplate(
#             template=GENERAL_PROMPT,
#             input_variables=["context", "question"]
#         )

#         # Step 4: Create QA chain with prompt
#         qa_chain = RetrievalQA.from_chain_type(
#             llm=llm,
#             chain_type="stuff",
#             retriever=retriever,
#             chain_type_kwargs={"prompt": prompt},
#             return_source_documents=False
#         )

#         # Step 5: Invoke chain with question
#         result = qa_chain.invoke({"query": question})
#         print(f"✅ Result (first 100 chars): {str(result)[:100]}")
#         return result

#     except Exception as e:
#         print(f"❌ Error in ask_general: {e}")
#         return f"❌ Error: {str(e)}"


def ask_general(question: str) -> str:
    print(f"\n⚡ ask_general called with question: {question}")
    try:
        # Step 1: Get context from raw texts
        context = "\n".join([chunk.strip() for chunk in get_raw_texts() if chunk.strip()])

        # Step 2: Create prompt
        prompt = PromptTemplate(
            template=GENERAL_PROMPT,
            input_variables=["context", "question"]
        )

        # Step 3: Create chain
        chain = LLMChain(llm=llm, prompt=prompt)

        # Step 4: Run chain
        result = chain.invoke({"context": context, "question": question})

        print(f"✅ Result (first 100 chars):{result}")
        return result['text']

    except Exception as e:
        print(f"❌ Error in ask_general: {e}")
        return f"❌ Internal error occurred: {str(e)}"

def get_raw_texts():
    from .document_loader import RAW_TEXTS
    return RAW_TEXTS