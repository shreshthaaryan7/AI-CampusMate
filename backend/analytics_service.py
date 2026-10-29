from backend.database import get_db_connection

def get_metrics_summary() -> dict:
    queries = {
        "faqs": "SELECT COUNT(*) FROM faqs", "notices": "SELECT COUNT(*) FROM notices",
        "queries": "SELECT COUNT(*) FROM query_logs", "unanswered": "SELECT COUNT(*) FROM query_logs WHERE is_answered=0",
        "tickets": "SELECT COUNT(*) FROM tickets", "open_tickets": "SELECT COUNT(*) FROM tickets WHERE status='Open'",
        "tasks": "SELECT COUNT(*) FROM tasks", "pending_tasks": "SELECT COUNT(*) FROM tasks WHERE status='Pending'",
        "feedback": "SELECT COUNT(*) FROM feedback"
    }
    with get_db_connection() as conn:
        return {key: conn.execute(sql).fetchone()[0] for key,sql in queries.items()}
