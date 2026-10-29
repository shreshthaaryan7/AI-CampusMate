from backend.database import get_db_connection

def get_all_faqs(search_query=None, category=None):
    sql = "SELECT * FROM faqs WHERE 1=1"
    args = []
    if search_query:
        sql += " AND (question LIKE ? OR answer LIKE ? OR category LIKE ?)"
        term = f"%{search_query}%"; args += [term, term, term]
    if category and category != "All":
        sql += " AND category = ?"; args.append(category)
    sql += " ORDER BY category, question"
    with get_db_connection() as conn:
        return conn.execute(sql, args).fetchall()

def add_faq(category, question, answer, source_label):
    with get_db_connection() as conn:
        cur = conn.execute("INSERT INTO faqs(category,question,answer,source_label) VALUES(?,?,?,?)", (category, question, answer, source_label or "Source not supplied"))
        return cur.lastrowid

def delete_faq(faq_id):
    with get_db_connection() as conn:
        conn.execute("DELETE FROM faqs WHERE id=?", (int(faq_id),))

def get_all_notices():
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM notices ORDER BY publish_date DESC, id DESC").fetchall()

def add_notice(title, content, publish_date, is_verified=0):
    with get_db_connection() as conn:
        cur = conn.execute("INSERT INTO notices(title,content,publish_date,is_verified) VALUES(?,?,?,?)", (title, content, publish_date, int(bool(is_verified))))
        return cur.lastrowid

def delete_notice(notice_id):
    with get_db_connection() as conn:
        conn.execute("DELETE FROM notices WHERE id=?", (int(notice_id),))

def search_passages(query, limit=5):
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM document_passages WHERE content LIKE ? ORDER BY id DESC LIMIT ?", (f"%{query}%", int(limit))).fetchall()
