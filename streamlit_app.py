import streamlit as st

# Define pages (put Lab 2 first so it’s the default selection)
pages = [
    st.Page("lab2.py", title="Lab 2"),
    st.Page("lab1.py", title="Lab 1"),
]

pg = st.navigation(pages)   # sidebar by default; use position="top" if you prefer a top nav
pg.run()