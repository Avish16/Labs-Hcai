import streamlit as st
from openai import OpenAI


# Load API key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)


# Updated title so you can tell it’s Lab 2
st.title("📄 Document question answering — Lab 2")

st.write(
    "This is the Lab 2 page."
)


uploaded_file = st.file_uploader("Upload a document (.txt or .md)", type=("txt", "md"))

question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

if uploaded_file and question:
        document = uploaded_file.read().decode(errors="ignore")
        messages = [{
            "role": "user",
            "content": f"Here's a document:\n\n{document}\n\n---\n\n{question}",
        }]

        stream = client.chat.completions.create(
            model="gpt-5-chat-latest",
            messages=messages,
            stream=True,
        )

        st.write_stream(stream)
