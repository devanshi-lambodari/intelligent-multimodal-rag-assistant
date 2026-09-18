# # import sys
# # from pathlib import Path

# # from fastapi import FastAPI
# # from pydantic import BaseModel


# # # Make sure Python can find the existing project files
# # SRC_DIR = Path(__file__).resolve().parent
# # sys.path.insert(0, str(SRC_DIR))

# # from langgraph_rag import run_langgraph_rag


# # # ==========================================================
# # # FASTAPI APP
# # # ==========================================================

# # app = FastAPI(
# #     title="Multimodal AI Chatbot API",
# #     description="RAG chatbot using Qdrant, Redis, LangGraph, Gemini and Tavily",
# #     version="1.0.0",
# # )


# # # ==========================================================
# # # REQUEST MODEL
# # # ==========================================================

# # class ChatRequest(BaseModel):
# #     question: str


# # # ==========================================================
# # # ROOT ENDPOINT
# # # ==========================================================

# # @app.get("/")
# # def root():
# #     return {
# #         "message": "Multimodal AI Chatbot API is running!"
# #     }


# # # ==========================================================
# # # CHAT ENDPOINT
# # # ==========================================================

# # @app.post("/chat")
# # def chat(request: ChatRequest):

# #     result = run_langgraph_rag(
# #         request.question,
# #         conversation_history=[]
# #     )

# #     return result








# import sys
# import logging
# from pathlib import Path
# from typing import Any, Optional

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field


# # ==========================================================
# # PROJECT PATH
# # ==========================================================

# SRC_DIR = Path(__file__).resolve().parent

# if str(SRC_DIR) not in sys.path:
#     sys.path.insert(0, str(SRC_DIR))


# # ==========================================================
# # EXISTING RAG PIPELINE
# # ==========================================================

# from langgraph_rag import run_langgraph_rag
# from redis_cache import is_redis_alive


# # ==========================================================
# # LOGGING
# # ==========================================================

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s | %(levelname)s | %(message)s"
# )

# logger = logging.getLogger(__name__)


# # ==========================================================
# # FASTAPI APPLICATION
# # ==========================================================

# app = FastAPI(
#     title="Multimodal AI Chatbot API",
#     description=(
#         "Backend API for a multimodal RAG chatbot using "
#         "LangGraph, Qdrant, Redis, Gemini, Tavily and runtime evaluation."
#     ),
#     version="1.0.0",
# )


# # ==========================================================
# # REQUEST MODELS
# # ==========================================================

# class ChatRequest(BaseModel):
#     question: str = Field(
#         ...,
#         min_length=1,
#         description="Question to ask the chatbot.",
#         examples=["Who is Sterling?"]
#     )


# # ==========================================================
# # RESPONSE MODELS
# # ==========================================================

# class EvaluationResult(BaseModel):
#     faithfulness: Optional[float] = None
#     context_precision: Optional[float] = None
#     answer_relevancy: Optional[float] = None


# class ChatResponse(BaseModel):
#     answer: str
#     source: str
#     document_found: bool
#     document_contexts: list[Any] = Field(default_factory=list)
#     web_results: list[Any] = Field(default_factory=list)
#     evaluation: EvaluationResult


# # ==========================================================
# # ROOT ENDPOINT
# # ==========================================================

# @app.get(
#     "/",
#     tags=["System"],
#     summary="API information"
# )
# def root():
#     return {
#         "name": "Multimodal AI Chatbot API",
#         "version": "1.0.0",
#         "status": "running",
#         "docs": "/docs",
#         "chat_endpoint": "/chat",
#         "health_endpoint": "/health",
#     }


# # ==========================================================
# # HEALTH CHECK
# # ==========================================================

# @app.get(
#     "/health",
#     tags=["System"],
#     summary="Check API and Redis health"
# )
# def health_check():

#     redis_status = is_redis_alive()

#     return {
#         "status": "healthy" if redis_status else "degraded",
#         "api": "running",
#         "redis": "connected" if redis_status else "unavailable",
#     }


# # ==========================================================
# # CHAT ENDPOINT
# # ==========================================================

# @app.post(
#     "/chat",
#     response_model=ChatResponse,
#     tags=["Chat"],
#     summary="Ask the RAG chatbot a question"
# )
# def chat(request: ChatRequest):

#     question = request.question.strip()

#     # ------------------------------------------------------
#     # Validate question
#     # ------------------------------------------------------

#     if not question:
#         raise HTTPException(
#             status_code=400,
#             detail="Question cannot be empty."
#         )

#     logger.info("Received chat request: %s", question)

#     try:

#         # --------------------------------------------------
#         # Run existing RAG pipeline
#         # --------------------------------------------------

#         result = run_langgraph_rag(
#             question,
#             conversation_history=[]
#         )

#         logger.info("Chat request completed successfully.")

#         return result

#     except Exception as e:

#         logger.exception("Chat request failed.")

#         raise HTTPException(
#             status_code=500,
#             detail=f"Chatbot processing failed: {str(e)}"
#         )









import sys
import logging
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field


# ==========================================================
# PROJECT PATH
# ==========================================================

SRC_DIR = Path(__file__).resolve().parent

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


# ==========================================================
# EXISTING RAG PIPELINE
# ==========================================================

from langgraph_rag import run_langgraph_rag
from redis_cache import is_redis_alive


# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ==========================================================
# FASTAPI APPLICATION
# ==========================================================

app = FastAPI(
    title="Multimodal AI Chatbot API",
    description=(
        "Backend API for a multimodal RAG chatbot using "
        "LangGraph, Qdrant, Redis, Gemini, Tavily and runtime evaluation."
    ),
    version="1.0.0",
)


# ==========================================================
# REQUEST MODEL
# ==========================================================

class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask the chatbot.",
        examples=["Who is Sterling?"]
    )


# ==========================================================
# RESPONSE MODELS
# ==========================================================

class EvaluationResult(BaseModel):
    faithfulness: Optional[float] = None
    context_precision: Optional[float] = None
    answer_relevancy: Optional[float] = None


class ChatResponse(BaseModel):
    answer: str
    source: str
    document_found: bool
    document_contexts: list[Any] = Field(default_factory=list)
    web_results: list[Any] = Field(default_factory=list)
    evaluation: EvaluationResult


# ==========================================================
# CHATBOT WEB PAGE
# ==========================================================

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Multimodal AI Chatbot</title>

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f5f7fb;
            color: #222;
        }

        .container {
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 25px;
        }

        .header h1 {
            margin-bottom: 8px;
        }

        .header p {
            color: #666;
            margin-top: 0;
        }

        .chat-box {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }

        .input-area {
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
        }

        #question {
            flex: 1;
            padding: 14px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 16px;
        }

        button {
            padding: 14px 22px;
            border: none;
            border-radius: 8px;
            background: #333;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background: #555;
        }

        button:disabled {
            background: #aaa;
            cursor: not-allowed;
        }

        .question {
            background: #f0f2f5;
            padding: 14px;
            border-radius: 8px;
            margin-bottom: 15px;
        }

        .answer {
            background: #fafafa;
            border-left: 4px solid #333;
            padding: 18px;
            border-radius: 8px;
            margin-bottom: 20px;
            line-height: 1.6;
        }

        .info {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-top: 15px;
        }

        .card {
            background: #f5f5f5;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
        }

        .card strong {
            display: block;
            margin-bottom: 5px;
        }

        .loading {
            color: #666;
            font-style: italic;
        }

        .error {
            color: #b00020;
            background: #ffecec;
            padding: 15px;
            border-radius: 8px;
        }

        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 13px;
            color: #777;
        }

        @media (max-width: 700px) {

            .input-area {
                flex-direction: column;
            }

            .info {
                grid-template-columns: 1fr;
            }

        }

    </style>
</head>


<body>

<div class="container">

    <div class="header">

        <h1>🤖 Multimodal AI Chatbot</h1>

        <p>
            Qdrant • Redis • LangGraph • Gemini • Tavily • RAG Evaluation
        </p>

    </div>


    <div class="chat-box">

        <div class="input-area">

            <input
                id="question"
                type="text"
                placeholder="Ask something..."
                autocomplete="off"
            >

            <button id="askButton" onclick="askQuestion()">
                Ask
            </button>

        </div>


        <div id="result"></div>

    </div>


    <div class="footer">

        API:
        <a href="/docs" target="_blank">Swagger Docs</a>
        &nbsp; | &nbsp;
        <a href="/health" target="_blank">Health</a>

    </div>

</div>


<script>

async function askQuestion() {

    const input = document.getElementById("question");
    const button = document.getElementById("askButton");
    const result = document.getElementById("result");

    const question = input.value.trim();

    if (!question) {
        result.innerHTML =
            '<div class="error">Please enter a question.</div>';
        return;
    }


    button.disabled = true;
    button.innerText = "Thinking...";


    result.innerHTML =
        '<div class="loading">🤔 Processing your question...</div>';


    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "Something went wrong."
            );

        }


        const faithfulness =
            data.evaluation?.faithfulness ?? "N/A";

        const contextPrecision =
            data.evaluation?.context_precision ?? "N/A";

        const relevancy =
            data.evaluation?.answer_relevancy ?? "N/A";


        result.innerHTML = `

            <div class="question">

                <strong>You:</strong>

                ${escapeHtml(question)}

            </div>


            <div class="answer">

                <strong>🤖 Answer</strong>

                <p>${escapeHtml(data.answer)}</p>

            </div>


            <div class="info">

                <div class="card">

                    <strong>Source</strong>

                    ${escapeHtml(data.source)}

                </div>


                <div class="card">

                    <strong>Faithfulness</strong>

                    ${faithfulness}

                </div>


                <div class="card">

                    <strong>Answer Relevancy</strong>

                    ${relevancy}

                </div>

            </div>

        `;

    }

    catch (error) {

        result.innerHTML = `

            <div class="error">

                ❌ ${escapeHtml(error.message)}

            </div>

        `;

    }

    finally {

        button.disabled = false;
        button.innerText = "Ask";

    }

}


/* Allow Enter key to submit */

document
    .getElementById("question")
    .addEventListener("keydown", function(event) {

        if (event.key === "Enter") {
            askQuestion();
        }

    });


/* Prevent HTML injection */

function escapeHtml(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;

}

</script>


</body>

</html>
"""


# ==========================================================
# ROOT → CHATBOT UI
# ==========================================================

@app.get(
    "/",
    response_class=HTMLResponse,
    tags=["System"],
    summary="Open chatbot interface"
)
def root():

    return HTML_PAGE


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.get(
    "/health",
    tags=["System"],
    summary="Check API and Redis health"
)
def health_check():

    redis_status = is_redis_alive()

    return {
        "status": "healthy" if redis_status else "degraded",
        "api": "running",
        "redis": "connected" if redis_status else "unavailable",
    }


# ==========================================================
# CHAT ENDPOINT
# ==========================================================

@app.post(
    "/chat",
    response_model=ChatResponse,
    tags=["Chat"],
    summary="Ask the RAG chatbot a question"
)
def chat(request: ChatRequest):

    question = request.question.strip()


    # ------------------------------------------------------
    # Validate question
    # ------------------------------------------------------

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )


    logger.info(
        "Received chat request: %s",
        question
    )


    try:

        # --------------------------------------------------
        # Run existing RAG pipeline
        # --------------------------------------------------

        result = run_langgraph_rag(
            question,
            conversation_history=[]
        )


        logger.info(
            "Chat request completed successfully."
        )


        return result


    except Exception as e:

        logger.exception(
            "Chat request failed."
        )


        raise HTTPException(
            status_code=500,
            detail=f"Chatbot processing failed: {str(e)}"
        )