DETAIL_SECTION_PROMPT_PDF = """
You are analyzing a tender document. Your task is to focus strictly on the section titled: '{title}'.

Section Content:
{content}

Instructions:
- Carefully analyze ONLY the section above and answer the question: "{question}".
- Do NOT refer to other sections unless this section explicitly points to them (e.g., “See Section X”).
- If there is such a reference, mention it briefly, but DO NOT elaborate or summarize the other section.
- Your response should be structured and clean for inclusion in a PDF document.
- Use clear headings, bullet points, or tables if applicable for better visual presentation in PDF.
- Avoid unnecessary repetition, verbose explanations, or decorative formatting like emojis.

Output Format Guidelines (for PDF):
- Begin your answer with a clear heading: `### Response for Section: {title}`
- Use bullet points for multiple items.
- Use a markdown-style table if structured data is present (e.g., deadlines, item specs).
- Keep paragraphs short and readable.
- Use proper line breaks and spacing to avoid dense blocks of text.

Return only the formatted answer for PDF inclusion.

Answer:
"""
