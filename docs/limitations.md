# StrataAI Known Limitations

This document tracks known limitations of the current architecture. These are intentionally left unaddressed until later weeks in the curriculum to ensure a step-by-step learning progression.

## 1. Streamlit "Amnesia" & Lack of Persistent Chat History
**Discovered in:** Week 4
**Symptom:** When a user refreshes the browser tab or closes the application, all chat history and active workspace context (`st.session_state.documents` and `st.session_state.messages`) are permanently wiped out.
**Root Cause:** Streamlit reruns the entire Python script on every interaction. We are using `st.session_state` as "Short-Term Memory", which is highly volatile and tied strictly to the active browser tab session.
**Future Solution (Week 6/7):** Introduce **Long-Term Memory** via an SQLite database. We will build a `Chat History` sidebar that saves `messages` and active `documents` to disk using SQLAlchemy/SQLite, allowing users to resume study sessions across multiple days.
