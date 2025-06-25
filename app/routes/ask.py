# app/routes/ask.py

from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse, StreamingResponse
from ..rag.query_classifier import is_detail_question,is_summary_question
from ..rag.query_engine import ask_summary, ask_detail,ask_general, ask_summary_pdf
from fpdf import FPDF
import io

router = APIRouter()

@router.post("/ask/")
async def ask_question(question: str = Form(...)):
    try:
        if is_detail_question(question):
            answer = ask_detail(question)
            return PlainTextResponse(answer)    
        elif is_summary_question(question):
            answer = ask_summary(question)
            return PlainTextResponse(answer)
        else:
            answer = ask_general(question)
            return PlainTextResponse(answer)
    except Exception as e:
        return PlainTextResponse(f"❌ Internal error occurred: {str(e)}", status_code=500)
    


@router.post("/ask/pdf/")
async def ask_pdf(question: str = Form(...), qtype: str = Form(...)):  # qtype: 'summary' or 'detail'
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        if qtype == "summary":
            result = ask_summary_pdf(question)
            content = "# Executive Summary\n\n" + result

        # elif qtype == "detail":
        #     responses = []
        #     for section_response in ask_detail_pdf(question):
        #         responses.append(section_response)
        #     content = "# Detailed Breakdown by Section\n\n" + "\n\n".join(responses)

        else:
            return PlainTextResponse("❌ Invalid type. Use 'summary' or 'detail'", status_code=400)

        # Add formatted text to PDF
        for line in content.split("\n"):
            if line.strip() == "":
                pdf.ln()
            else:
                pdf.multi_cell(0, 10, line)

        # Save to in-memory buffer
        pdf_buffer = io.BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)

        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=tender_{qtype}.pdf"}
        )

    except Exception as e:
        return PlainTextResponse(f"❌ Error generating PDF: {str(e)}", status_code=500)