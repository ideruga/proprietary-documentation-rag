# app.py
import os
from flask import Flask, render_template, request, jsonify
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from process_pdfs import process_pdfs
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

app = Flask(__name__)

# Set your OpenAI API key
# os.environ["OPENAI_API_KEY"] = 'your-openai-api-key'  # Replace with your key or set it as an environment variable

# Process PDFs during server startup
pdf_directory = 'docs'  # Directory containing your PDFs
vectorstore_path = 'vectorstore'  # Directory to save the vector store

if not os.path.exists(vectorstore_path):
    os.makedirs(vectorstore_path)
    vectorstore = process_pdfs(pdf_directory)
    vectorstore.save_local(vectorstore_path)
else:
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)

# Initialize the Conversational Retrieval Chain
llm = OpenAI(temperature=0)
qa_chain = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever())

# Route for the chat interface
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint for handling chat messages
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    chat_history = data.get('history', [])

    response = qa_chain({"question": user_message, "chat_history": chat_history})
    answer = response['answer']

    # Update chat history
    chat_history.append((user_message, answer))

    return jsonify({'answer': answer, 'history': chat_history})

if __name__ == '__main__':
    app.run(debug=True)
