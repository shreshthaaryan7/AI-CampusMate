<<<<<<< HEAD
# AI CampusMate — AI-Powered College Helpdesk Prototype

AI CampusMate is a local Streamlit demonstration app for campus FAQs, cautious knowledge-base question answering, PDF text indexing, support tickets, a task planner, notice/FAQ management, and record-based analytics.

> **Important:** The bundled FAQs and notices are fictional demonstration content. This prototype is not connected to a real college system, does not verify institutional policies, and does not send tickets to college staff. Replace demo records with approved sources before real use. The administration console has no authentication and must not be exposed publicly.

## Technology
- Python + Streamlit interface
- SQLite local persistence
- pandas for tables and simple charts
- PyMuPDF for selectable-text PDF extraction
- Transparent keyword retrieval and intent rules; no paid API key or external LLM required

## Structure
```text
AI-CampusMate/
├── frontend/
│   ├── app.py
│   ├── ui_helpers.py
│   └── assets/styles.css
├── backend/
│   ├── database.py
│   ├── security.py
│   ├── sample_data.py
│   ├── knowledge_base.py
│   ├── intent_classifier.py
│   ├── retrieval_engine.py
│   ├── answer_engine.py
│   ├── document_processor.py
│   ├── ticket_service.py
│   ├── planner_service.py
│   └── analytics_service.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example
```
Only `frontend/` and `backend/` are application folders at the top level. SQLite creates `campusmate.db` on first run; it is excluded from Git.

## Run on Windows / VS Code
Open a terminal in the `AI-CampusMate` project root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run frontend/app.py
```
If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` in that terminal and activate again. Alternatively use `.venv\Scripts\python.exe -m streamlit run frontend/app.py` after installing packages into that environment.

## Seven pages
1. **Campus Overview** — metrics, searchable FAQs, and notices.
2. **AI Intelligence Center** — question matching, source labels, fallback, feedback.
3. **Knowledge Hub** — category/search filters and PDF extraction/indexing with page metadata.
4. **Student Services** — create and view locally stored tickets.
5. **Smart Campus Planner** — due dates, categories, priorities, completion, deletion, overdue status.
6. **Administration Console** — local demo FAQ/notice management and ticket status controls.
7. **Intelligence & Analytics** — SQLite-backed counts and charts.

## How the question answering works
Question → simple intent rules → keyword overlap retrieval over FAQ questions → PDF passage keyword search → answer with source label or safe fallback. This is not a trained model or an LLM. A matched FAQ is not automatically an official/verified source; students should confirm policies with the institution.

## PDF processing
Text-based PDFs up to 5 MB and 100 pages are supported. Extracted text is stored locally with filename and page number and can be retrieved by keyword. OCR for scanned PDFs is not included. Uploaded documents are untrusted; only upload files you have permission to process.

## Data and privacy
- All records are stored in a local SQLite file (`campusmate.db` by default).
- Set `CAMPUSMATE_DB_PATH` to change its location.
- Do not commit database files, credentials, or private student data to GitHub.
- There is no login/authorization. The admin page is intended for a local presentation only.
- No real college notices, policy documents, or student system integration are included.

## Presentation walkthrough
1. Show the overview and explain that records are demo data.
2. Search the Knowledge Hub for an FAQ.
3. Ask a matching question and show the source label; then ask an unrelated question to demonstrate fallback.
4. Upload a small text-based PDF and show extracted page text.
5. Create a ticket and add/complete a planner task.
6. Use the local admin console to add a demo FAQ or notice and change a ticket status.
7. Show analytics changing as records are created.

## Manual verification checklist
- [ ] All seven pages load without exceptions.
- [ ] A supported FAQ question returns a match and source label.
- [ ] An unrelated question returns a fallback rather than a fabricated answer.
- [ ] Feedback saves successfully.
- [ ] A ticket remains after app refresh.
- [ ] Planner tasks can be added, completed, deleted, and marked overdue.
- [ ] PDF extraction rejects non-PDF, oversized, damaged, and textless files.
- [ ] Metrics update after creating records.

## Known limitations / future work
- No authentication or role-based access control.
- Keyword retrieval can miss paraphrases and is not semantic search.
- PDF OCR, embeddings, LLM-generated grounded summaries, editing existing FAQs, and institutional integrations are not implemented.
- No automated test suite is included yet; manually verify all workflows before presenting.
=======
# AI-CampusMate
>>>>>>> 95673034975101402876d97a9d861d9f0f22d811
