from backend.retrieval_engine import find_best_match
from backend.intent_classifier import classify_intent
from backend.database import get_db_connection

def process_student_question(question: str) -> dict:
    question = (question or "").strip()
    if not question:
        return {"status":"empty", "answer":"Please enter a question.", "source":None, "log_id":None}
    intent = classify_intent(question)
    match = find_best_match(question)
    with get_db_connection() as conn:
        cur = conn.execute("INSERT INTO query_logs(question,detected_intent,is_answered) VALUES(?,?,?)", (question, intent, 1 if match else 0))
        log_id = cur.lastrowid
    if match:
        return {"status":"success", "answer":match["answer"], "source":match.get("source_label", "Source not supplied"), "intent":intent, "log_id":log_id, "score":match.get("score"), "source_type":match.get("source_type", "FAQ")}
    return {"status":"fallback", "answer":"I couldn't find sufficiently relevant evidence in the current knowledge base. I won't guess about official college rules. Check your institution's official website or create a support ticket in Student Services.", "source":None, "intent":intent, "log_id":log_id}

def log_feedback(log_id: int, rating: str, comments: str=""):
    if rating not in {"Helpful", "Not helpful"}: raise ValueError("Invalid feedback rating")
    with get_db_connection() as conn:
        conn.execute("INSERT INTO feedback(log_id,rating,comments) VALUES(?,?,?)", (int(log_id), rating, (comments or "")[:1000]))
