def classify_intent(question: str) -> str:
    q = question.lower()
    if any(k in q for k in ["exam", "test", "quiz", "paper", "grade"]):
        return "Examinations"
    if any(k in q for k in ["fee", "pay", "cost", "cash", "fine"]):
        return "Fees"
    if any(k in q for k in ["scholarship", "stipend", "aid"]):
        return "Scholarships"
    if any(k in q for k in ["admission", "join", "seat", "document"]):
        return "Admissions"
    if any(k in q for k in ["schedule", "time", "calendar", "hour"]):
        return "Timetables"
    return "General Campus Query"
