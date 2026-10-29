"""Safe PDF text extraction. Uploaded documents are untrusted input."""
from pathlib import Path
from backend.database import get_db_connection
MAX_BYTES = 5 * 1024 * 1024
MAX_PAGES = 100

def parse_pdf_preview(uploaded_file) -> dict:
    name = Path(getattr(uploaded_file, "name", "upload.pdf")).name
    if not name.lower().endswith(".pdf"):
        return {"status":"error", "message":"Only PDF files are supported."}
    data = uploaded_file.getvalue()
    if not data or len(data) > MAX_BYTES:
        return {"status":"error", "message":"PDF is empty or exceeds the 5 MB limit."}
    if not data.startswith(b"%PDF-"):
        return {"status":"error", "message":"The uploaded file does not appear to be a valid PDF."}
    try:
        import fitz
        doc = fitz.open(stream=data, filetype="pdf")
        if doc.page_count > MAX_PAGES:
            doc.close(); return {"status":"error", "message":f"PDF exceeds the {MAX_PAGES}-page limit."}
        pages = []
        for i, page in enumerate(doc):
            text = page.get_text("text").strip()
            if text:
                pages.append({"page":i+1, "text":text[:12000]})
        doc.close()
        if not pages:
            return {"status":"error", "message":"No selectable text was found. The PDF may be scanned; OCR is not included."}
        with get_db_connection() as conn:
            for p in pages:
                conn.execute("INSERT INTO document_passages(filename,page_number,content) VALUES(?,?,?)", (name, p["page"], p["text"]))
        return {"status":"success", "filename":name, "extracted_pages":pages, "stored_pages":len(pages)}
    except Exception:
        return {"status":"error", "message":"The PDF could not be read. Check that it is not damaged or password-protected."}
