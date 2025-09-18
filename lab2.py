import streamlit as st
from openai import OpenAI

# --- Keys via Streamlit Secrets ONLY ---
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY)

st.title("🧾 Lab 2C: Summarization (4o / 4o-mini)")

# Upload input
uploaded_file = st.file_uploader("Upload a document (.txt or .md)", type=("txt", "md"))

# Sidebar controls
with st.sidebar:
    st.header("Summary options")
    summary_style = st.radio(
        "Choose summary type",
        ["100 words", "2 paragraphs", "5 bullet points"],
        index=0
    )
    use_advanced = st.checkbox("Use Advanced Model (4o)", value=False)
    model = "gpt-4o" if use_advanced else "gpt-4o-mini"

def build_instruction(style: str) -> str:
    if style == "100 words":
        return "Summarize the document in ~100 words. Be concise and faithful."
    if style == "2 paragraphs":
        return "Summarize the document in exactly two connected paragraphs; paragraph 2 should build on paragraph 1."
    return "Summarize the document as exactly 5 concise bullet points capturing distinct key ideas."

def summarize(document: str, style: str, model_name: str):
    instruction = build_instruction(style)
    messages = [
        {"role": "system", "content": "You are a careful summarizer. Preserve meaning and avoid fabrications."},
        {"role": "user", "content": f"{instruction}\n\n---\nDOCUMENT:\n{document}\n---"}
    ]
    stream = client.chat.completions.create(
        model=model_name,
        messages=messages,
        stream=True,
        temperature=0.2,
    )
    return stream

# Auto-run once a file is selected
if uploaded_file:
    text = uploaded_file.read().decode(errors="ignore")
    st.subheader(f"Model: {model}")
    st.caption(f"Summary type: {summary_style}")
    with st.spinner("Generating summary..."):
        st.write_stream(summarize(text, summary_style, model))
else:
    st.info("Upload a .txt or .md file to see the summary.", icon="📄")
