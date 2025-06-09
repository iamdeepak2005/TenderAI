from langchain.llms.base import LLM
from typing import Optional, List
import requests
import PyPDF2
import os

# Custom Ollama LLM class
class OllamaLLM(LLM):
    model: str = "deepseek-r1:7b"
    base_url: str = "http://localhost:11434"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json()["response"]

    @property
    def _llm_type(self) -> str:
        return "ollama"

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

# Split text into manageable chunks (optional for large PDFs)
def split_text(text: str, max_chars: int = 2000) -> List[str]:
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

# Main function
def summarize_pdf(pdf_path: str):
    llm = OllamaLLM()
    full_text = extract_text_from_pdf(pdf_path)
    chunks = split_text(full_text)

    summaries = []
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}...")
        prompt = f"Summarize the following text:\n\n{chunk}"
        summary = llm.invoke(prompt)
        summaries.append(summary)

    final_summary = "\n\n".join(summaries)
    print("\n===== FINAL SUMMARY =====\n")
    print(final_summary)

# Example usage
if __name__ == "__main__":
    pdf_file_path = r"C:\Users\deepa\Downloads\Gem-tender.pdf"  # Change this to your actual PDF path
    summarize_pdf(pdf_file_path)
