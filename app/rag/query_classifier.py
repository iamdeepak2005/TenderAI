# app/rag/query_classifier.py

SUMMARY_KEYWORDS = ["summary", "overview", "brief", "highlights"]
DETAIL_KEYWORDS = ["clause", "article", "chapter", "specific", "explain", "in detail"]

def is_summary_question(question: str) -> bool:
    return any(word in question.lower() for word in SUMMARY_KEYWORDS)

def is_detail_question(question: str) -> bool:
    return any(word in question.lower() for word in DETAIL_KEYWORDS)
