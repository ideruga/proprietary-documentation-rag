import os

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma


def process_pdfs(pdf_directory, embeddings, persistent_directory):
    documents = []
    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            filepath = os.path.join(pdf_directory, filename)
            loader = PyPDFLoader(filepath)
            documents = loader.load()
            for doc in documents:
                doc.metadata = {"filename": filename}
            documents.extend(documents)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    vectorstore = Chroma.from_documents(
        docs, embeddings, persist_directory=persistent_directory)

    return vectorstore
