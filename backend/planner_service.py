from datetime import date
from backend.database import get_db_connection

def add_task(description: str, due_date: str, category: str, priority: str):
    date.fromisoformat(due_date)
    if priority not in {"Low", "Medium", "High"}: raise ValueError("Invalid priority")
    with get_db_connection() as conn:
        cur = conn.execute("INSERT INTO tasks(description,due_date,category,priority,status) VALUES(?,?,?,?, 'Pending')", (description, due_date, category, priority))
        return cur.lastrowid

def get_tasks():
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM tasks ORDER BY CASE status WHEN 'Pending' THEN 0 ELSE 1 END, due_date ASC").fetchall()
def complete_task(task_id: int):
    with get_db_connection() as conn: conn.execute("UPDATE tasks SET status='Completed' WHERE id=?", (int(task_id),))
def delete_task(task_id: int):
    with get_db_connection() as conn: conn.execute("DELETE FROM tasks WHERE id=?", (int(task_id),))
