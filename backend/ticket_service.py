import uuid
from backend.database import get_db_connection
ALLOWED_STATUSES = {"Open", "In Progress", "Resolved", "Closed"}
def create_ticket(category: str, subject: str, description: str) -> str:
    with get_db_connection() as conn:
        while True:
            ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
            if not conn.execute("SELECT 1 FROM tickets WHERE id=?", (ticket_id,)).fetchone(): break
        conn.execute("INSERT INTO tickets(id,category,subject,description,status) VALUES(?,?,?,?, 'Open')", (ticket_id, category, subject, description))
    return ticket_id
def get_tickets():
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM tickets ORDER BY created_at DESC").fetchall()
def update_ticket_status(tkt_id: str, status: str):
    if status not in ALLOWED_STATUSES: raise ValueError("Invalid ticket status")
    with get_db_connection() as conn:
        conn.execute("UPDATE tickets SET status=? WHERE id=?", (status, tkt_id))
