# Flask Chat Application with OpenAI and LangChain RAG

## Description

This project is designed to enable interactive conversations with a Large Language Model (LLM) that are enriched with information from proprietary PDF documentation files. 

---

## Features

- **Conversational Interface**: Web-based chat interface built with Flask.
- **Retrieval-Augmented Generation**: Integrates LangChain to enhance responses with information from local PDFs.
- **PDF Processing**: Automatically processes and indexes PDFs during startup.
- **Persistent Vector Store**: Saves the vector store locally to avoid reprocessing.
- **Dockerized Deployment**: Provides a Docker image for easy deployment, available on GitHub Container Registry.

---

## Running the Application

### Option 1: Run from GitHub Container Registry

#### Step 1: Pull the Docker Image

```
docker pull ghcr.io/ideruga/proprietary-documentation-rag:latest
```

#### Step 2: Prepare PDF Directory

Create a directory on your host machine to store PDFs.

```
mkdir /path/to/your/pdfs
```

Place your PDF files into this directory.

#### Step 3: Run the Docker Container

```
docker run -d -p 5000:5000 \
  -e OPENAI_API_KEY=your-openai-api-key \
  -v /path/to/your/pdfs:/app/docs \
  ghcr.io/ideruga/proprietary-documentation-rag:latest
```

- **Environment Variables**:
  - `OPENAI_API_KEY`: Your OpenAI API key.
- **Volume Mount**:
  - Mount your local PDFs directory to `/app/pdfs` inside the container.

#### Step 4: Access the Application

Open your browser and navigate to `http://localhost:5000`.

---

### Option 2: Build and Run Docker Image Locally

#### Step 1: Clone the Repository

```
git clone https://github.com/ideruga/proprietary-documentation-rag.git
cd proprietary-documentation-rag
```

#### Step 2: Prepare PDF Directory

Place your PDF files into the `docs` directory in the project root.

```
mkdir docs
# Copy your PDF files into the 'docs' directory
```

#### Step 3: Build the Docker Image

```
docker build -t proprietary-documentation-rag:latest .
```

#### Step 4: Run the Docker Container

```
docker run -d -p 5000:5000 \
  -e OPENAI_API_KEY=your-openai-api-key \
  proprietary-documentation-rag:latest
```

- **Note**: If you have PDFs in a local directory, mount it to the container:

```
docker run -d -p 5000:5000 \
  -e OPENAI_API_KEY=your-openai-api-key \
  -v $(pwd)/pdfs:/app/docs \
  proprietary-documentation-rag:latest
```

#### Step 5: Access the Application

Open your browser and navigate to `http://localhost:5000`.

---

## Project Structure

- **app.py**: Main Flask application.
- **process_pdfs.py**: Processes PDFs and builds the vector store.
- **requirements.txt**: Python dependencies.
- **Dockerfile**: Builds the Docker image.
- **templates/index.html**: HTML template for the chat interface.
- **pdfs/**: Directory containing PDF documents.
- **vectorstore/**: Directory where the vector store is saved.

---


## Security Considerations

- **API Key Management**: Do not hardcode your OpenAI API key. Pass it as an environment variable.
- **Dangerous Deserialization**: The application uses pickle for serialization. Set `LANGCHAIN_ALLOW_DANGEROUS_SERIALIZATION=true` only if you trust the source.
- **Input Validation**: Ensure proper input validation to prevent security vulnerabilities.

---

## License

This project is licensed under the MIT License.

---

Feel free to reach out if you have any questions or need further assistance!
