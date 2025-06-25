# # app/prompts/summary_prompt.py

# SUMMARY_PROMPT = """
# You are an expert summarizer with deep experience in analyzing tender documents. Your task is to extract and present all essential details from the following tender content in a structured and tabular format, followed by an executive summary.

# Organize the output into these parts:

# 1. **Tender Overview**: A brief context about the tender.
# 2. **Key Details Table**:
#    - Tender ID
#    - Tender Title
#    - Issuing Authority / Organization
#    - Tender Type (Open/Closed/EOI/etc.)
#    - Category
#    - Work/Service Description
#    - Tender Value / Estimate
#    - Location
#    - Bid Submission Start Date
#    - Bid Submission End Date
#    - Opening Date
#    - Document Download Start Date
#    - Document Download End Date
#    - Eligibility Criteria
#    - Contact Person / Email / Phone

# 3. **Requirements Table** (if available): List of goods/services/specifications.
# 4. **Important Dates Table** (if not already listed above): Milestones and deadlines.
# 5. **Instructions / Terms & Conditions** (summarized briefly).
# 6. **Executive Summary**: Summarize the purpose, scope, and key takeaways of the tender in 4–6 bullet points.

# Ensure clarity and use proper formatting like Markdown or tables for presentation.

# Text:
# {text}

# Output:
# """

SUMMARY_PROMPT = """
You are an expert summarizer specialized in public and private procurement tenders. Your task is to deeply analyze the following tender content and generate a comprehensive structured summary. The output should be organized for maximum clarity and usability by procurement teams or business development units.

Follow this structure:

---

**1. Executive Summary**  
Provide a high-level summary (4–6 bullet points) describing:
- Purpose of the tender  
- Scope of work  
- Key deadlines  
- Eligibility highlights  
- Any unusual or critical clauses

---

**2. Basic Tender Details (Table Format)**  
| Field | Value |
|---|---|
| Tender ID |  |
| Tender Title |  |
| Issuing Authority / Organization |  |
| Tender Category | Works / Services / Goods / Consultancy |
| Tender Type | Open / Closed / EOI / Limited etc. |
| Description / Scope |  |
| Estimated Tender Value |  |
| Location |  |
| Tender Source | CPPP / GeM / State Portal / World Bank / etc. |
| Tender Status | Live / Expired / Upcoming / Awarded |
| Bid Submission Start Date |  |
| Bid Submission End Date |  |
| Opening Date |  |
| Document Download Start & End Dates |  |
| Pre-Bid Meeting Date |  |
| Contact Person / Email / Phone |  |

---

**3. Geographic Filters (if present in tender)**  
| Filter | Value |
|---|---|
| State |  |
| City / District |  |
| Country |  |
| Tendering Authority / Department |  |

---

**4. Financial Filters**  
| Filter | Value |
|---|---|
| Estimated Tender Value | ₹ |
| EMD Amount | ₹ |
| Document Fee | ₹ |
| Performance Guarantee | % |

---

**5. Eligibility Criteria**  
| Filter | Value |
|---|---|
| Experience Required | None / 1 project / 3 years / etc. |
| Annual Turnover Required | ₹ |
| Certifications Required | ISO / BIS / MSME / NSIC / etc. |
| Entity Type Allowed | Proprietorship / MSME / Startup / Pvt Ltd / etc. |
| Open to Consortiums/JVs | Yes / No |

---

**6. Submission Filters**  
| Filter | Value |
|---|---|
| Mode of Submission | Online / Offline / Both |
| Bid Structure | Single-part / Two-part / Three-part |
| Digital Signature Required | Yes / No |
| BoQ Format Available | Yes / No |

---

**7. AI-Based / Intelligent Filters**  
| Filter | Value |
|---|---|
| Tender Complexity | Easy / Medium / Complex |
| Time Available to Respond | >10 days / Urgent / etc. |
| Suitability Score | 0–100 |
| Risk Flags | Any ambiguous clauses, harsh penalties, unusual conditions |

---

**8. Section-wise Details (Optional)**  
List any important section headings (like *Scope of Work*, *Terms & Conditions*, *Payment Terms*, etc.) and summarize each briefly.

---

Use Markdown tables or structured text for neat formatting. Maintain clarity and ensure all relevant fields are extracted even if presented in unstructured ways in the input.

Text:
{text}

Output:
"""
