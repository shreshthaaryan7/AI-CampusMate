"""Transparent keyword retrieval with conservative matching; not an LLM."""
import re
from backend.database import get_db_connection
from backend.knowledge_base import search_passages
STOP = {"where","what","when","how","can","the","is","are","for","to","of","a","an","i","my","do","does","in","on","and","or","please","tell","me","about","find","get"}
def tokens(text):
    return {t for t in re.findall(r"[a-z0-9]+", (text or "").lower()) if len(t) > 1 and t not in STOP}
def find_best_match(question):
    q = tokens(question)
    if not q: return None
    with get_db_connection() as conn:
        faqs = conn.execute("SELECT * FROM faqs").fetchall()
    best = None; best_score = 0.0
    for faq in faqs:
        qt = tokens(faq["question"]); at = tokens(faq["answer"])
        if not qt: continue
        # Favor question-term overlap and require enough of the user's meaningful terms to match.
        overlap = len(q & qt)
        score = (overlap / max(len(q), 1)) * 0.75 + (overlap / max(len(qt), 1)) * 0.25
        if overlap >= 2 and score > best_score:
            best, best_score = faq, score
    if best and best_score >= 0.34:
        return {**dict(best), "score": round(best_score, 3), "source_type": "FAQ"}
    # Document passages are searched only for meaningful terms; citations include page number.
    for term in sorted(q, key=len, reverse=True):
        passages = search_passages(term, 5)
        if passages:
            p = passages[0]
            return {"answer": p["content"], "source_label": f"{p['filename']} — page {p['page_number']}", "score": 0.35, "source_type": "PDF passage"}
    return None
