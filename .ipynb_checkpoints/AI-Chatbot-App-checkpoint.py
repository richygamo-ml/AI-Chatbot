import streamlit as st
from dotenv import load_dotenv
import os
from datetime import datetime

from langchain_community.document_loaders import TextLoader, CSVLoader, PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is not set. Check your .env file or terminal environment.")

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Financial Assistant",
    page_icon="💰",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color:#0E1117;
    color:white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

messages = st.session_state.messages

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("💰 Finance AI")

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload knowledge file",
        type=["txt", "pdf", "csv"]
    )

    st.markdown("---")

    st.subheader("Capabilities")
    st.write("• Investment basics")
    st.write("• Personal finance")
    st.write("• Budgeting advice")

    st.markdown("---")

    st.metric("Messages", len(messages))

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    chat_text = ""
    for m in messages:
        role = "User" if m["role"] == "user" else "AI"
        chat_text += f"{role}: {m['content']}\n\n"

    st.download_button(
        "Download Chat",
        chat_text,
        file_name="chat.txt"
    )

# ---------------- TITLE ----------------

st.title("💰 AI Financial Assistant")

st.caption(
    "Ask questions about investing, budgeting, and personal finance."
)

st.divider()

# ---------------- LOAD DOCUMENTS ----------------

documents = []

if uploaded_file:

    os.makedirs("temp", exist_ok=True)
    file_path = os.path.join("temp", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if uploaded_file.name.endswith(".txt"):
        loader = TextLoader(file_path)

    elif uploaded_file.name.endswith(".pdf"):
        loader = PyPDFLoader(file_path)

    elif uploaded_file.name.endswith(".csv"):
        loader = CSVLoader(file_path)

    documents = loader.load()

else:

    if os.path.exists("documents/knowledge.txt"):
        loader = TextLoader("documents/knowledge.txt")
        documents = loader.load()

# ---------------- VECTOR STORE ----------------

vectorstore = None
retriever = None

if documents:

    splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = splitter.split_documents(documents)

    docs = [d for d in docs if d.page_content and d.page_content.strip()]

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectorstore = Chroma.from_documents(docs, embeddings)

    retriever = vectorstore.as_retriever(search_kwargs={"k":3})

# ---------------- LLM ----------------

llm = ChatOpenAI(
    temperature=0,
    streaming=True
)

# ---------------- DISPLAY CHAT ----------------

for msg in messages:

    if msg["role"] == "user":

        with st.chat_message("user"):
            st.write(msg["content"])
            st.caption(msg["time"])

    else:

        with st.chat_message("assistant"):
            st.write(msg["content"])
            st.caption(msg["time"])

# ---------------- USER INPUT ----------------

user_input = st.chat_input("Ask a finance question...")

if user_input and retriever:

    time_now = datetime.now().strftime("%H:%M")

    messages.append({
        "role": "user",
        "content": user_input,
        "time": time_now
    })

    with st.chat_message("user"):
        st.write(user_input)
        st.caption(time_now)

    docs = retriever.invoke(user_input)

    context = " ".join([d.page_content for d in docs])

    prompt = f"""
Context:
{context}

Question:
{user_input}
"""

    with st.chat_message("assistant"):

        placeholder = st.empty()
        full_response = ""

        for chunk in llm.stream(prompt):

            if chunk.content:
                full_response += chunk.content
                placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

    messages.append({
        "role": "assistant",
        "content": full_response,
        "time": datetime.now().strftime("%H:%M")
    })

    with st.expander("Sources Used"):
        for d in docs:
            st.write(d.page_content[:300])