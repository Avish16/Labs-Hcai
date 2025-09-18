import streamlit as st

# App meta
st.set_page_config(page_title="Labs Manager", page_icon="🧪", layout="wide")

# Order matters: first page is the default
pages = [
    st.Page("lab4.py", title="Lab 4 — Vector DB", icon="🧪"),
    st.Page("lab3.py", title="Lab 3 — Chatbot", icon="💬"),
    st.Page("lab2.py", title="Lab 2 — Summarization", icon="🧾"),
    st.Page("lab1.py", title="Lab 1 — Document QA", icon="📄"),
]

nav = st.navigation(pages)   # sidebar by default; use position="top" for a top nav
nav.run()
