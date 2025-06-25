SUMMARY_PROMPT_PDF = """
You are an expert summarizer. Read the following tender content and generate a professional executive summary.

Text:
{text}

Instructions:
- Provide a concise and structured summary highlighting the key aspects of the tender.
- Include important details such as scope, eligibility, deadlines, submission process, and evaluation criteria—**only if they are present** in the text.
- The summary must be well-formatted for inclusion in a PDF document.
- Use clear section headings (e.g., ## Scope, ## Eligibility) where appropriate.
- Prefer bullet points or markdown tables for structured data like timelines or requirements.
- Avoid copying large verbatim text; rephrase and summarize meaningfully.
- Ensure proper line spacing and readability—no dense paragraphs.

Output Format Guidelines:
- Start with: `# Executive Summary`
- Use `##` for each subsection (if applicable)
- Use bullet points or tables when listing items
- Do not include external references or speculative content

Return only the formatted summary, ready to be inserted into a PDF report.

Summary:
"""
