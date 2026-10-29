"""Clearly fictional sample data for demonstration; never treat as official policy."""
from backend.database import get_db_connection

DEMO_FAQS = [
("Examinations", "Where can I find the examination timetable?", "This demonstration app does not know your institution's official timetable. Check the official college website or examination office.", "DEMO ONLY — replace with official source"),
("Admissions", "What is the admission procedure?", "Admission procedures vary by institution and programme. Consult the official admissions portal for current steps and deadlines.", "DEMO ONLY — official admissions portal required"),
("Documents", "Which documents may be required for admission?", "Institutions may request identity proof, prior academic records, photographs, and other documents. Confirm the exact list in the official admission notice.", "DEMO ONLY — verify current checklist"),
("Fees", "When is the semester fee deadline?", "I cannot verify a current fee deadline from this demo knowledge base. Check the official student portal or accounts office.", "DEMO ONLY — official finance notice required"),
("Scholarships", "How do I apply for a scholarship?", "Check the official scholarship notice for eligibility, required documents, deadlines, and application steps. Do not rely on unofficial messages for financial decisions.", "DEMO ONLY — official scholarship notice required"),
("Timetables", "Where can I access my class timetable?", "Check the official department notice board or student portal. This demo does not contain your real section timetable.", "DEMO ONLY — official timetable required"),
("Student support", "How can I contact student support?", "Use the Student Services page to create a support ticket in this local demo. For real assistance, use your institution's official support channels.", "AI CampusMate demo workflow"),
("Notice verification", "How do I verify whether a notice is genuine?", "Confirm the notice on an official institution domain or with the issuing department. Verify the date and issuing authority before acting.", "General guidance — confirm with institution"),
("Applications", "How can I request an official transcript?", "Transcript procedures and fees vary. Check the registrar's official instructions or contact the registrar directly.", "DEMO ONLY — official registrar guidance required"),
("Using CampusMate", "What should I do if CampusMate cannot answer?", "Create a ticket in Student Services and include enough detail for the support team. The current prototype stores tickets locally on this device.", "AI CampusMate demo workflow"),
]

def insert_sample_data():
    with get_db_connection() as conn:
        if conn.execute("SELECT COUNT(*) FROM faqs").fetchone()[0] == 0:
            conn.executemany("INSERT INTO faqs(category,question,answer,source_label) VALUES(?,?,?,?)", DEMO_FAQS)
        if conn.execute("SELECT COUNT(*) FROM notices").fetchone()[0] == 0:
            conn.executemany("INSERT INTO notices(title,content,publish_date,is_verified) VALUES(?,?,?,0)", [
                ("Welcome to AI CampusMate", "This is a demonstration notice, not an official college announcement. Replace it with an approved notice before deployment.", "2026-10-30"),
                ("Knowledge base setup reminder", "Administrators should add current, approved institutional information and its source before students rely on answers.", "2026-10-30")
            ])
