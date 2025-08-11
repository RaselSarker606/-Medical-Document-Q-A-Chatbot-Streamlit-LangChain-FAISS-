# 🏥 Medical Document Q&A Chatbot (Streamlit + LangChain + Gemini + FAISS)

## 📖 Overview
A **smart medical assistant** that turns your uploaded medical PDFs—like lab reports, prescriptions, or discharge summaries—into an interactive Q&A experience.  
Using **Streamlit** for the UI, **LangChain** for orchestration, **FAISS** for semantic search, and **Google Gemini Pro 2.5** for language understanding, it delivers **fast, precise, and context-aware** answers.  


---

## 📂 Key Features
- 📤 **Drag-and-Drop Medical PDF Upload**
- 🔍 **Semantic Search with FAISS** – Finds the most relevant parts of your medical document.
- 🧠 **LLM-Powered Responses** – Context-aware answers using Google Gemini.
- 🛡 **No Hallucinations** – Only answers from document content.
- 💻 **Streamlit Interactive UI** – Instant answers without technical setup.

---

## 🛠 Tools, Libraries, and Packages
- **Python 3.8+**
- **Streamlit** – User interface
- **LangChain** – LLM orchestration
- **FAISS** – Vector search
- **Google Generative AI (Gemini Pro 2.5)** – Answer generation
- **SentenceTransformers** – Embedding generation
- **PyPDF2** – PDF text extraction
- **dotenv** – Environment variable handling
- **pickle** – Caching embeddings

---

## 🚀 Setup Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/medical-document-chatbot.git
cd medical-document-chatbot
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Add Your API Key
Create a `.env` file in the root folder:
```
GOOGLE_API_KEY=your-api-key-here
```

### 4️⃣ Run the App
```bash
streamlit run main.py
```
Go to `http://localhost:8501/` in your browser.

---

## 💬 Sample Queries & Outputs

**English Queries**
- "What is the patient’s diagnosis?"
- "List all prescribed medicines."
- "What does the blood report say about hemoglobin?"


**Example Output:**
```
Q: What is the patient’s diagnosis?
A: The patient has Type 2 Diabetes Mellitus.
```

---

## 📌 Prompt Rules
- Answer only from uploaded document content.
- Keep answers short and relevant.

---

## 📄 API Documentation (If Implemented)
- `POST /upload` – Upload PDF file.
- `POST /ask` – Ask a question about the document.
- `GET /answer` – Retrieve the generated answer.

---

## 📊 Evaluation Matrix (Example)
| Metric         | Value |
|----------------|-------|
| Accuracy       | 90%   |
| Precision      | 88%   |
| Recall         | 92%   |
| MRR (Top-3)    | 0.94  |

---

## 🧠 Submission Q&A

**1. What method/library did you use to extract text and why?**  
We used **PyPDF2** for reliable extraction from structured medical PDFs. Some required extra whitespace & newline cleanup.

---

🚀 **Turn any medical PDF into an instant question-answer tool — just upload, ask, and get precise answers in seconds.**
