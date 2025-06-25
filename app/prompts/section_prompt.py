DETAIL_SECTION_PROMPT = """
You are analyzing a tender document. Your task is to focus **only** on the section titled: '{title}'.

Section Content:
{content}

Instructions:
- Read only the above section and answer the following question: "{question}".
- Do not use any information from other sections unless it is explicitly referenced in this section.
- If this section refers to another section, briefly mention the link (e.g., "See Section X"), but do not explain it in detail.
- Avoid repeating the full context or summarizing the entire document.
- Keep the response precise and relevant only to this section.

Answer:
"""
