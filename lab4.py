import os
import sys
import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader

# --- Fix for ChromaDB on Streamlit Cloud ---
__import__("pysqlite3")
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import chromadb
from chromadb.utils import embedding_functions

st.title("Lab 4")

# ------------------------
# Init OpenAI client
# ------------------------
if "openai_client" not in st.session_state:
    api_key = st.secrets["OPENAI_API_KEY"]
    st.session_state.openai_client = OpenAI(api_key=api_key)

# ------------------------
# Setup ChromaDB with OpenAI embeddings
# ------------------------
chromaDB_path = "./ChromaDB_for_lab"
chroma_client = chromadb.PersistentClient(path=chromaDB_path)

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=st.secrets["OPENAI_API_KEY"],
    model_name="text-embedding-3-small"  # 1536-dim
)

# Always drop + recreate collection each run (avoid stale UUIDs / dimension errors)
try:
    chroma_client.delete_collection("Lab4Collection")
except Exception:
    pass

st.session_state.Lab4_vectorDB = chroma_client.create_collection(
    name="Lab4Collection",
    embedding_function=openai_ef,
)

# ------------------------
# PDF loader
# ------------------------
def read_pdf(path: str) -> str:
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# ------------------------
# Build collection once
# ------------------------
PDF_DIR = "file_folder/lab4_pdfs"

if "Lab4_loaded" not in st.session_state:
    pdfs = [f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]
    docs, ids, metas = [], [], []
    for i, pdf in enumerate(pdfs, start=1):
        text = read_pdf(os.path.join(PDF_DIR, pdf))
        if not text.strip():
            st.warning(f"⚠️ No text extracted from {pdf}, skipping.")
            continue
        docs.append(text)
        ids.append(f"doc_{i}")
        metas.append({"filename": pdf})
    if docs:
        st.session_state.Lab4_vectorDB.add(documents=docs, ids=ids, metadatas=metas)
        st.success(f"✅ Added {len(docs)} documents to vector DB.")
    else:
        st.error("❌ No valid text found in PDFs.")
    st.session_state.Lab4_loaded = True
else:
    st.info("Using cached Vector DB.")

# ------------------------
# Querying demo
# ------------------------
topic = st.selectbox("Pick a test topic", ["Generative AI", "Text Mining", "Data Science Overview"])

if st.button("Run search"):
    openai_client = st.session_state.openai_client
    response = openai_client.embeddings.create(
        input=topic,
        model="text-embedding-3-small",  # 1536-dim
    )
    query_embedding = response.data[0].embedding

    results = st.session_state.Lab4_vectorDB.query(
        query_embeddings=[query_embedding],
        n_results=3,
    )

    if results["metadatas"]:
        st.write("Top 3 results:")
        for i, md in enumerate(results["metadatas"][0], start=1):
            st.write(f"{i}. {md['filename']}")
    else:
        st.warning("⚠️ No results returned. Check if PDFs had extractable text.")
