import datetime as dt
import pandas as pd
import streamlit as st

from frontend.ui_helpers import apply_custom_ui
from backend.database import init_db
from backend.sample_data import insert_sample_data
from backend.knowledge_base import get_all_faqs, get_all_notices, add_faq, add_notice, delete_faq, delete_notice
from backend.answer_engine import process_student_question, log_feedback
from backend.document_processor import parse_pdf_preview
from backend.ticket_service import create_ticket, get_tickets, update_ticket_status
from backend.planner_service import add_task, get_tasks, complete_task, delete_task
from backend.analytics_service import get_metrics_summary
from backend.security import sanitize_input, validate_ticket_payload, validate_text

st.set_page_config(page_title="AI CampusMate", page_icon="🎓", layout="wide")
init_db(); insert_sample_data(); apply_custom_ui()

st.sidebar.title("🎓 AI CampusMate")
st.sidebar.caption("Student helpdesk · local demonstration prototype")
pages = ["🏛️ Campus Overview", "🧠 AI Intelligence Center", "📚 Knowledge Hub", "🛠️ Student Services", "📅 Smart Campus Planner", "🎛️ Administration Console", "📊 Intelligence & Analytics"]
selected_page = st.sidebar.radio("Navigate", pages)
st.sidebar.divider()
st.sidebar.warning("Demo data is fictional unless explicitly marked otherwise. Verify official college information before acting.")

def df_rows(rows):
    return pd.DataFrame([dict(r) for r in rows]) if rows else pd.DataFrame()

def metric(label, value, help_text=None):
    st.metric(label, value, help=help_text)

if selected_page == "🏛️ Campus Overview":
    st.title("Campus Overview")
    st.write("A central place to explore campus information, ask questions, track support requests, and plan academic tasks.")
    m = get_metrics_summary()
    cols = st.columns(4)
    for c, label, value in zip(cols, ["Knowledge FAQs", "Notices", "Open tickets", "Pending tasks"], [m['faqs'], m['notices'], m['open_tickets'], m.get('pending_tasks', 0)]):
        c.metric(label, value)
    st.info("This is a local prototype. Sample notices and FAQs are demonstration records, not official college announcements.")
    left, right = st.columns([1.2, 1])
    with left:
        st.subheader("Search the knowledge base")
        search = st.text_input("Search FAQs and answers", key="overview_search", placeholder="e.g. scholarship, timetable, transcript")
        rows = get_all_faqs(search_query=search) if search else get_all_faqs()
        for f in rows[:5]:
            with st.expander(f"{f['category']}: {f['question']}"):
                st.write(f['answer']); st.caption(f"Source label: {f['source_label']}")
    with right:
        st.subheader("Latest notices")
        for n in get_all_notices()[:5]:
            with st.container(border=True):
                st.markdown(f"**{n['title']}**")
                st.caption(f"{n['publish_date']} · {'Approved' if n['is_verified'] else 'Demo / unverified'}")
                st.write(n['content'])

elif selected_page == "🧠 AI Intelligence Center":
    st.title("AI Intelligence Center")
    st.caption("Transparent keyword-based retrieval prototype — not a generative LLM. Answers are limited to available FAQ records and uploaded PDF text.")
    st.write("Try: *Where can I find the examination timetable?* or ask a question not covered by the knowledge base to see the safe fallback.")
    with st.form("ask_form", clear_on_submit=False):
        question = st.text_area("Your campus question", placeholder="Ask about admissions, exams, fees, scholarships, or student services…", max_chars=1000)
        submitted = st.form_submit_button("Search knowledge base", type="primary")
    if submitted:
        if not question.strip(): st.warning("Please enter a question first.")
        else:
            result = process_student_question(sanitize_input(question, 1000))
            st.session_state["last_answer"] = {"question":question, **result}
    result = st.session_state.get("last_answer")
    if result:
        st.markdown(f"**Question:** {result['question']}")
        if result["status"] == "success":
            st.success(result["answer"])
            st.caption(f"Matched source: {result.get('source') or 'Source not supplied'} · Type: {result.get('source_type','FAQ')} · Intent: {result.get('intent','General')}")
            st.caption("A match is not proof that a source is official. Confirm institutional policies with the issuing office.")
        else:
            st.warning(result["answer"])
        if result.get("log_id"):
            with st.form(f"feedback_{result['log_id']}"):
                rating = st.radio("Was this response useful?", ["Helpful", "Not helpful"], horizontal=True)
                comments = st.text_input("Optional feedback", max_chars=500)
                if st.form_submit_button("Submit feedback"):
                    try:
                        log_feedback(result["log_id"], rating, sanitize_input(comments, 500)); st.success("Feedback saved locally.")
                    except Exception as exc: st.error(f"Could not save feedback: {exc}")
    st.subheader("Suggested questions")
    st.write("Examination timetable · Admission documents · Scholarship process · Verify a notice · What if CampusMate cannot answer?")

elif selected_page == "📚 Knowledge Hub":
    st.title("Knowledge Hub")
    st.write("Search FAQs and inspect their source labels. The demo records are not official policies.")
    c1, c2 = st.columns([2,1])
    with c1: query = st.text_input("Search knowledge", key="hub_query")
    categories = sorted({r['category'] for r in get_all_faqs()})
    with c2: category = st.selectbox("Category", ["All"] + categories)
    faqs = get_all_faqs(search_query=query or None, category=category)
    st.caption(f"{len(faqs)} FAQ record(s) found")
    for f in faqs:
        with st.expander(f"{f['category']} · {f['question']}"):
            st.write(f['answer']); st.caption(f"Source label: {f['source_label']} · Updated: {f['updated_at']}")
    st.divider(); st.subheader("Upload a text-based PDF")
    st.caption("Extracted page text is stored locally for keyword search. Only upload documents you are allowed to use; scanned PDFs need OCR, which is not included.")
    upload = st.file_uploader("Choose a PDF (max 5 MB, max 100 pages)", type=["pdf"])
    if upload and st.button("Extract and index PDF"):
        parsed = parse_pdf_preview(upload)
        if parsed["status"] != "success": st.error(parsed["message"])
        else:
            st.success(f"Extracted and indexed {parsed['stored_pages']} page(s) from {parsed['filename']}.")
            for p in parsed["extracted_pages"][:5]:
                with st.expander(f"Page {p['page']}"): st.text(p['text'][:3000])

elif selected_page == "🛠️ Student Services":
    st.title("Student Services")
    st.write("Create a local support ticket and track its status. This prototype does not send tickets to your actual college.")
    with st.form("ticket_form"):
        category = st.selectbox("Category", ["Academic", "Admissions", "Fees", "IT Support", "Scholarships", "Other"])
        subject = st.text_input("Subject", max_chars=150)
        description = st.text_area("Describe the issue", max_chars=2000)
        send = st.form_submit_button("Create support ticket", type="primary")
    if send:
        if validate_ticket_payload(category, subject, description):
            ticket_id = create_ticket(category, sanitize_input(subject,150), sanitize_input(description,2000)); st.success(f"Ticket created: {ticket_id}")
        else: st.error("Please enter a subject and description. Subject max 150 characters; description max 2,000 characters.")
    st.subheader("Ticket register")
    tickets = get_tickets()
    if tickets: st.dataframe(df_rows(tickets), use_container_width=True, hide_index=True)
    else: st.info("No tickets yet. Create one above to test persistence.")

elif selected_page == "📅 Smart Campus Planner":
    st.title("Smart Campus Planner")
    with st.form("task_form"):
        description = st.text_input("Task name", max_chars=200)
        c1,c2,c3 = st.columns(3)
        due = c1.date_input("Due date", value=dt.date.today() + dt.timedelta(days=1))
        category = c2.selectbox("Category", ["Academic", "Personal", "Project", "Exam", "Other"])
        priority = c3.selectbox("Priority", ["Low", "Medium", "High"])
        if st.form_submit_button("Add task", type="primary"):
            if description.strip(): add_task(sanitize_input(description,200), due.isoformat(), category, priority); st.success("Task saved."); st.rerun()
            else: st.error("Enter a task name.")
    tasks = get_tasks()
    if not tasks: st.info("No tasks yet. Add one above.")
    for t in tasks:
        due_date = dt.date.fromisoformat(t['due_date'])
        overdue = t['status'] == 'Pending' and due_date < dt.date.today()
        with st.container(border=True):
            c1,c2,c3 = st.columns([3,1,1])
            c1.markdown(f"**{t['description']}**")
            c1.caption(f"{t['category']} · {t['priority']} priority · Due {t['due_date']}")
            c2.write("🔴 Overdue" if overdue else ("✅ Completed" if t['status']=='Completed' else "🟡 Pending"))
            if t['status'] == 'Pending' and c3.button("Complete", key=f"complete_{t['id']}"):
                complete_task(t['id']); st.rerun()
            elif c3.button("Delete", key=f"delete_{t['id']}"):
                delete_task(t['id']); st.rerun()

elif selected_page == "🎛️ Administration Console":
    st.title("Administration Console")
    st.warning("LOCAL DEMO — no authentication or role-based authorization is implemented. Do not expose this console publicly or enter real private student data.")
    tab_faq, tab_notice, tab_tickets, tab_manage = st.tabs(["Add FAQ", "Add notice", "Manage tickets", "Manage records"])
    with tab_faq:
        with st.form("faq_admin"):
            cat = st.selectbox("Category", ["Examinations", "Admissions", "Documents", "Fees", "Scholarships", "Timetables", "Student support", "Other"])
            fq = st.text_input("Question", max_chars=500); fa = st.text_area("Answer", max_chars=5000); src = st.text_input("Source label (required for traceability)", max_chars=250)
            if st.form_submit_button("Save FAQ"):
                if validate_text(fq,500) and validate_text(fa,5000): add_faq(cat, sanitize_input(fq,500), sanitize_input(fa,5000), sanitize_input(src,250) or "Source not supplied"); st.success("FAQ saved locally.")
                else: st.error("Question and answer are required.")
    with tab_notice:
        with st.form("notice_admin"):
            title = st.text_input("Notice title", max_chars=250); content = st.text_area("Notice content", max_chars=5000); pub_date = st.date_input("Publication date", value=dt.date.today()); approved = st.checkbox("Approved by an authorized institution representative", value=False)
            if st.form_submit_button("Save notice"):
                if validate_text(title,250) and validate_text(content,5000): add_notice(sanitize_input(title,250), sanitize_input(content,5000), pub_date.isoformat(), approved); st.success("Notice saved. Its approval flag reflects your checkbox; the app cannot independently verify it.")
                else: st.error("Title and content are required.")
    with tab_tickets:
        tickets = get_tickets()
        if tickets:
            for t in tickets:
                c1,c2,c3 = st.columns([3,1,1]); c1.write(f"**{t['id']}** · {t['subject']}"); c1.caption(f"{t['category']} · {t['created_at']}")
                status = c2.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"], index=["Open","In Progress","Resolved","Closed"].index(t['status']) if t['status'] in ["Open","In Progress","Resolved","Closed"] else 0, key=f"status_{t['id']}")
                if c3.button("Update", key=f"update_{t['id']}"): update_ticket_status(t['id'], status); st.success("Ticket status updated."); st.rerun()
        else: st.info("No tickets to manage.")
    with tab_manage:
        st.subheader("FAQs")
        for f in get_all_faqs():
            c1,c2 = st.columns([5,1]); c1.write(f"{f['id']}. {f['question']}")
            if c2.button("Delete", key=f"faqdel_{f['id']}"): delete_faq(f['id']); st.rerun()
        st.subheader("Notices")
        for n in get_all_notices():
            c1,c2 = st.columns([5,1]); c1.write(f"{n['id']}. {n['title']} ({'approved flag' if n['is_verified'] else 'demo/unverified'})")
            if c2.button("Delete", key=f"noticedel_{n['id']}"): delete_notice(n['id']); st.rerun()

elif selected_page == "📊 Intelligence & Analytics":
    st.title("Intelligence & Analytics")
    st.caption("Metrics are calculated from the local SQLite records; they are not measures of AI accuracy.")
    m = get_metrics_summary()
    rows = [("FAQs",m['faqs']),("Notices",m['notices']),("Questions asked",m['queries']),("Unanswered questions",m['unanswered']),("All tickets",m['tickets']),("Open tickets",m['open_tickets']),("All tasks",m['tasks']),("Pending tasks",m.get('pending_tasks',0)),("Feedback records",m['feedback'])]
    for start in range(0,len(rows),3):
        cols = st.columns(3)
        for col,(label,value) in zip(cols,rows[start:start+3]): col.metric(label,value)
    st.subheader("Answered versus unanswered questions")
    if m['queries']:
        st.bar_chart(pd.DataFrame({"Count":[m['queries']-m['unanswered'],m['unanswered']]}, index=["Matched", "Fallback"]))
    else: st.info("Ask questions in AI Intelligence Center to populate this chart.")
    st.subheader("Ticket status distribution")
    tickets = get_tickets()
    if tickets:
        tdf = df_rows(tickets)
        st.bar_chart(tdf["status"].value_counts())
    else: st.info("Create tickets to populate ticket analytics.")
