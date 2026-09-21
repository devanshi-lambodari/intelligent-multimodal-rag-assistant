# Intelligent Multimodal RAG Assistant

An end-to-end **Retrieval-Augmented Generation (RAG)** application that combines document understanding, semantic search, vector retrieval, OCR, web search fallback, LLM generation, caching, runtime evaluation, and a FastAPI interface.

## 🚀 Overview

The **Intelligent Multimodal RAG Assistant** is designed to answer questions using information retrieved from documents and provide a web-search fallback when relevant information cannot be found in the available document context.

The project demonstrates a complete AI application workflow:

**Documents → Parsing → Chunking → Embeddings → Semantic Search → Vector Retrieval → RAG → Web Fallback → LLM Generation → Evaluation → Caching → API**

The goal of this project was to build an AI system that goes beyond simply connecting an LLM to a prompt by incorporating retrieval, orchestration, caching, evaluation, and API development.

---

## ✨ Features

* 📚 **Retrieval-Augmented Generation (RAG)** for answering questions using relevant document context
* 🔎 **Semantic Search** using vector embeddings
* 🧠 **BAAI/bge-small-en-v1.5** for generating document and query embeddings
* 🗄️ **Qdrant** for vector storage and similarity search
* ✂️ **Document chunking and preprocessing** for improved retrieval
* 🖼️ **OCR processing** for scanned and image-based documents
* 🤖 **Google Gemini** for context-aware response generation
* 🌐 **Tavily Web Search** as a fallback when relevant information is not found in the provided documents
* 🔗 **LangGraph** for workflow orchestration
* ⚡ **Redis caching** to reduce repeated processing and improve response efficiency
* 📊 **RAG evaluation** using Faithfulness, Context Precision, and Answer Relevancy
* 🧪 **Runtime evaluation** of generated responses
* 🚀 **FastAPI** for API access and interactive web interface
* 🐙 **Git & GitHub** for version control and project management

---

## 🏗️ Architecture

```text
                    User Question
                          │
                          ▼
                      FastAPI
                          │
                          ▼
                    Redis Cache
                    /          \
                 HIT            MISS
                  │               │
                  ▼               ▼
               Answer         LangGraph
                                  │
                                  ▼
                               Qdrant
                                  │
                                  ▼
                         Document Retrieval
                            /          \
                         Found       Not Found
                           │             │
                           ▼             ▼
                        Gemini        Tavily
                           │             │
                           └──────┬──────┘
                                  │
                                  ▼
                         Runtime Evaluation
                                  │
                                  ▼
                            Redis Cache
                                  │
                                  ▼
                               Answer
```

---

## 🔄 RAG Workflow

### 1. Document Processing

Documents are parsed and prepared for processing.

### 2. Chunking

Documents are divided into smaller chunks to improve retrieval relevance.

### 3. Embedding Generation

Document chunks are converted into vector embeddings using:

```text
BAAI/bge-small-en-v1.5
```

### 4. Vector Storage

The generated embeddings are stored in **Qdrant**.

### 5. Query Embedding

When a user asks a question, the query is converted into an embedding using the same embedding model.

### 6. Semantic Retrieval

Qdrant performs similarity search to retrieve the most relevant document chunks.

### 7. Response Generation

If relevant document context is available, **Gemini** generates an answer based on the retrieved context.

### 8. Web Search Fallback

If the required information cannot be found in the provided documents, **Tavily** performs a web search to retrieve additional information.

### 9. Runtime Evaluation

The generated response can be evaluated using metrics such as:

* Faithfulness
* Context Precision
* Answer Relevancy

### 10. Redis Caching

The generated answer is cached in Redis so repeated questions can be answered more efficiently.

---

## 🛠️ Tech Stack

| Technology                 | Purpose                                |
| -------------------------- | -------------------------------------- |
| **Python**                 | Core programming language              |
| **Google Gemini**          | LLM-based response generation          |
| **LangGraph**              | AI workflow orchestration              |
| **Qdrant**                 | Vector database and semantic retrieval |
| **BAAI/bge-small-en-v1.5** | Text embeddings                        |
| **Tavily**                 | Web search fallback                    |
| **Redis**                  | Response caching                       |
| **PaddleOCR**              | OCR for image/scanned documents        |
| **FastAPI**                | REST API and web interface             |
| **Uvicorn**                | ASGI server                            |
| **RAGAS**                  | RAG evaluation                         |
| **Git & GitHub**           | Version control                        |

---

## 📁 Project Structure

```text
intelligent-multimodal-rag-assistant/
│
├── evaluation/
│   ├── evaluation_dataset.csv
│   ├── evaluation_results.csv
│   ├── rag_results.csv
│   └── test_question.py
│
├── src/
│   ├── api.py
│   ├── check_db.py
│   ├── chunking.py
│   ├── document_parser.py
│   ├── embedding.py
│   ├── evaluate_rag.py
│   ├── gemini_client.py
│   ├── image_utils.py
│   ├── ingestion.py
│   ├── langgraph_rag.py
│   ├── ocr_utils.py
│   ├── redis_cache.py
│   ├── retrieval.py
│   └── runtime_evaluator.py
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md
└── requirements.txt
```

---

## ⚙️ Getting Started

### Prerequisites

Make sure you have the following installed:

* Python 3.11+
* Git
* Redis
* Qdrant
* Google Gemini API key
* Tavily API key

---

### 1. Clone the Repository

```bash
git clone https://github.com/devanshi-lambodari/intelligent-multimodal-rag-assistant.git
cd intelligent-multimodal-rag-assistant
```

---

### 2. Create a Virtual Environment

#### Windows PowerShell

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

**Never commit your `.env` file or API keys to GitHub.**

---

## ▶️ Running the Application

Start the FastAPI application using:

```bash
python -m uvicorn src.api:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### Interactive API Documentation

FastAPI automatically provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

The application also provides a browser-based interface for interacting with the RAG assistant.

---

## 🔌 API

### `GET /`

Returns the web interface for interacting with the assistant.

### `GET /health`

Checks the application's health and Redis connectivity.

### `POST /chat`

Accepts a user question and returns the generated answer along with relevant response information.

Example request:

```json
{
  "question": "What information is available in the documents?"
}
```

---

## 📊 Evaluation

The project includes both **offline evaluation** and **runtime evaluation**.

### Evaluation Metrics

#### Faithfulness

Measures whether the generated answer is supported by the retrieved context.

#### Context Precision

Measures how relevant the retrieved context is to the expected answer.

#### Answer Relevancy

Measures how relevant the generated response is to the user's question.

Evaluation datasets and results are stored in the:

```text
evaluation/
```

directory.

---

## ⚡ Redis Caching

Redis is used to cache generated answers.

The workflow is:

```text
User Question
      ↓
Redis Cache Check
   ↙          ↘
 HIT          MISS
  ↓             ↓
Answer      RAG Pipeline
                ↓
             Answer
                ↓
          Store in Redis
```

This prevents repeated questions from unnecessarily triggering the complete retrieval and generation pipeline.

---

## 🌐 Web Search Fallback

The assistant follows a document-first approach.

```text
User Question
      ↓
Qdrant Retrieval
      ↓
Relevant Context?
   ↙          ↘
 YES           NO
  ↓             ↓
Gemini        Tavily
  ↓             ↓
Answer        Answer
```

**Tavily** is used only as a fallback when relevant information cannot be obtained from the provided document context.

---

## 🐳 Docker

A Dockerfile is included for containerized deployment.

Build the image:

```bash
docker build -t intelligent-multimodal-rag-assistant .
```

Run the container:

```bash
docker run -p 8000:8000 intelligent-multimodal-rag-assistant
```

The application will then be available at:

```text
http://localhost:8000
```

---

## 🔐 Security

Sensitive configuration values are stored using environment variables.

The following files and directories are excluded from version control:

```text
.env
venv/
qdrant_db/
__pycache__/
```

API keys should never be hardcoded into the source code or committed to GitHub.

---

## 📌 Future Improvements

Potential future improvements include:

* Cloud deployment
* Qdrant Cloud integration
* Managed Redis deployment
* Improved multimodal document understanding
* Advanced retrieval strategies
* Hybrid search combining semantic and keyword retrieval
* Improved evaluation datasets
* Authentication and user management
* Conversation history and persistent sessions
* Performance monitoring and observability

---

## 🎯 Learning Outcomes

This project provided hands-on experience with:

* Generative AI
* Retrieval-Augmented Generation
* Semantic search
* Vector databases
* Embeddings
* OCR
* LLM integration
* AI workflow orchestration
* Web search integration
* Caching
* RAG evaluation
* REST APIs
* FastAPI
* Git and GitHub
* Application architecture

---

## 📄 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author

**Devanshi Lambodari**

GitHub: [devanshi-lambodari](https://github.com/devanshi-lambodari)

Project: [Intelligent Multimodal RAG Assistant](https://github.com/devanshi-lambodari/intelligent-multimodal-rag-assistant)
