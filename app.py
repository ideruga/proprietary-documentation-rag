# app.py
import os
from flask import Flask, render_template, request, jsonify
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from process_pdfs import process_pdfs
from langchain.embeddings.openai import OpenAIEmbeddings

app = Flask(__name__)

pdf_directory = 'docs'
vectorstore_path = 'vectorstore'

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

if not os.path.exists(vectorstore_path):
    os.makedirs(vectorstore_path)
    vectorstore = process_pdfs(pdf_directory, embeddings, vectorstore_path)
else:
    vectorstore = Chroma(persist_directory=vectorstore_path, embedding_function=embeddings)

llm = ChatOpenAI(model="gpt-4o", temperature=0.5)

contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, just "
    "reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

qa_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful documentation guru. You are tasked with answering questions based on the documentation."
     "If you can't derive the answer from the documentation, just say so."
     "\n\n"
     "{context}"),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

qa_chain = create_stuff_documents_chain(llm, qa_prompt)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},
)

history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    chat_history = data.get('history', [])



    messages = []
    for human, ai in chat_history:
        messages.append(HumanMessage(content=human))
        messages.append(AIMessage(content=ai))


    result = rag_chain.invoke({"input": user_message, "chat_history": messages})
    answer = result['answer']

    chat_history.append((user_message, answer))

    return jsonify({'answer': answer, 'history': chat_history})

if __name__ == '__main__':
    app.run(debug=True)
