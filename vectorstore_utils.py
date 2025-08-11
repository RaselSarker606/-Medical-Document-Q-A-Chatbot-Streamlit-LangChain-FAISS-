from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List

def create_faiss_index(texts: List[str]):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    return FAISS.from_texts(texts, embeddings)

def retrieve_relevant_docs(vectorstore, query: str, k: int =3):
    docs = vectorstore.similarity_search(query, k=k)
    return docs
