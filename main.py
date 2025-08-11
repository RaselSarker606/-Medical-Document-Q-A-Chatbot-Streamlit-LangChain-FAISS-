import streamlit as st
import time
import faiss

from ui import pdf_uploader
from pdf_utils import extract_text_from_pdf
from vectorstore_utils import create_faiss_index, retrieve_relevant_docs
from chat_utils import get_google_chat_model, ask_chat_model
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI


# ------------------ Streamlit Page Configuration ------------------ #
st.set_page_config(
    page_title="Medical Document Assistant (RAG System)",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ------------------ Custom Styling ------------------ #
st.markdown("""
    <style>
        /* Background */
        body {
            background-color: #f0f4f8;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #dbe9ff;
            padding: 20px 15px 30px 15px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgb(0 0 0 / 0.1);
        }

        /* Sidebar headers */
        .sidebar .stMarkdown h2 {
            font-weight: 700;
            color: #0b3d91;
            margin-bottom: 10px;
        }

        /* Chat messages bubbles */
        .stChatMessage {
            border-radius: 15px;
            padding: 18px 20px;
            margin-bottom: 12px;
            max-width: 75%;
            word-wrap: break-word;
            font-size: 17px;
            line-height: 1.5;
            box-shadow: 0 2px 6px rgb(0 0 0 / 0.07);
        }

        .stChatMessage.user {
            background-color: #d0e8ff;
            color: #0b3d91;
            text-align: right;
            margin-left: auto;
            margin-right: 10px;
        }

        .stChatMessage.assistant {
            background-color: #fff5e6;
            color: #7a4f01;
            text-align: left;
            margin-right: auto;
            margin-left: 10px;
        }

        /* Message timestamp */
        .stCaption {
            font-size: 12px;
            color: #777;
            margin-top: -10px;
            margin-bottom: 10px;
            font-style: italic;
        }

        /* Headers */
        h1, h2, h3, h4, h5 {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: 600;
            color: #0b3d91;
        }

        /* Chat input */
        .stTextInput>div>input {
            font-size: 16px !important;
            padding: 10px 15px !important;
            border-radius: 8px !important;
            border: 1.5px solid #0b3d91 !important;
        }

        /* Footer */
        footer {
            text-align: center;
            font-size: 0.85rem;
            color: #666;
            margin-top: 30px;
            padding-bottom: 15px;
        }

        /* Button */
        div.stButton > button:first-child {
            background-color: #0b3d91;
            color: white;
            padding: 10px 24px;
            font-size: 16px;
            border-radius: 8px;
            border: none;
            transition: background-color 0.3s ease;
        }

        div.stButton > button:first-child:hover {
            background-color: #08408b;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)


# ------------------ Initialize Session States ------------------ #
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "chat_model" not in st.session_state:
    st.session_state.chat_model = None


# ------------------ Sidebar: Upload Documents ------------------ #
with st.sidebar:
    st.markdown("### 📂 Document Upload")
    st.markdown("Upload your medical documents to get started.")

    uploaded_files = pdf_uploader()

    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} document(s) uploaded successfully.")

        if st.button("Process Documents"):
            with st.spinner("Processing documents, please wait..."):
                # Extract text from uploaded PDFs
                all_texts = [extract_text_from_pdf(file) for file in uploaded_files]

                # Split into chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len
                )

                chunks = []
                for text in all_texts:
                    chunks.extend(text_splitter.split_text(text))

                # Create FAISS index and initialize chat model
                st.session_state.vectorstore = create_faiss_index(chunks)
                st.session_state.chat_model = get_google_chat_model()

            st.success("Documents processed successfully!")


# ------------------ Main Chat Interface ------------------ #
st.markdown("### 💬 Chat with your medical documents")


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        st.caption(message["timestamp"])


# ------------------ Chat Input ------------------ #
prompt = st.chat_input("Ask about your medical documents...")

if prompt:
    timestamp = time.strftime("%H:%M")

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": timestamp
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(timestamp)

    # Check if vectorstore and model exist
    if st.session_state.vectorstore and st.session_state.chat_model:
        with st.chat_message("assistant"):
            with st.spinner("Searching documents..."):
                # Retrieve relevant context
                relevant_docs = retrieve_relevant_docs(
                    st.session_state.vectorstore,
                    prompt
                )

                context = "\n\n".join([doc.page_content for doc in relevant_docs])

                system_prompt = f"""
You are DocuChat Pro, an intelligent document assistant.
Based on the following documents, provide accurate and helpful answers.
If the answer is not in the documents, say: "The information is not available in the document."
"

Medical Documents:
{context}

User Question: {prompt}

Answer:
"""

                response = ask_chat_model(
                    st.session_state.chat_model,
                    system_prompt
                )

            # Display response
            st.markdown(response)
            st.caption(timestamp)

            # Store assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": timestamp
            })

    else:
        with st.chat_message("assistant"):
            st.error("⚠️ Please upload and process documents first!")
            st.caption(timestamp)


# ------------------ Footer ------------------ #
st.markdown("___")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    🤖 Powered by AI with RASEL | 🏥 Medical Document Assistant (RAG System)
</div>
""", unsafe_allow_html=True)
