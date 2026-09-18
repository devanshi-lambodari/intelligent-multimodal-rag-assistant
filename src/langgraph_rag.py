# import os
# from typing import TypedDict, List

# from dotenv import load_dotenv
# from langgraph.graph import StateGraph, START, END
# from langchain_tavily import TavilySearch

# from retrieval import (
#     retrieve,
#     build_context,
#     get_node_text,
#     build_retrieval_query,
#     call_gemini,
#     GEMINI_MODEL,
#     FALLBACK_MODEL,
#     MAX_RETRIES,
#     INITIAL_RETRY_DELAY,
# )

# import time


# # ==========================================================
# # LOAD ENVIRONMENT
# # ==========================================================

# load_dotenv()

# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# if not TAVILY_API_KEY:
#     raise RuntimeError(
#         "TAVILY_API_KEY not found in .env file."
#     )


# # ==========================================================
# # TAVILY SEARCH
# # ==========================================================

# tavily_search = TavilySearch(
#     max_results=5,
#     topic="general",
# )


# # ==========================================================
# # LANGGRAPH STATE
# # ==========================================================

# class GraphState(TypedDict):

#     # User's original question
#     question: str

#     # Previous conversation
#     conversation_history: List[dict]

#     # Query actually sent to Qdrant
#     retrieval_query: str

#     # Retrieved Qdrant results
#     retrieved_results: list

#     # Extracted document contexts
#     document_contexts: List[str]

#     # Formatted context
#     document_context: str

#     # Answer generated from documents
#     document_answer: str

#     # Whether documents could answer the question
#     document_found: bool

#     # Tavily results
#     web_results: List[dict]

#     # Final answer
#     final_answer: str

#     # Source of final answer
#     source: str


# # ==========================================================
# # GEMINI WITH RETRY + FALLBACK
# # ==========================================================

# def generate_with_fallback(prompt: str):

#     """
#     Calls Gemini with retries.

#     Primary model:
#         gemini-3.6-flash

#     Fallback:
#         gemini-3.5-flash
#     """

#     def try_model(model_name):

#         for attempt in range(
#             1,
#             MAX_RETRIES + 1,
#         ):

#             try:

#                 print(
#                     f"\n🤖 Trying {model_name} "
#                     f"(attempt {attempt}/{MAX_RETRIES})..."
#                 )

#                 answer = call_gemini(
#                     model=model_name,
#                     prompt=prompt,
#                 )

#                 print(
#                     f"✅ {model_name} responded successfully."
#                 )

#                 return answer

#             except Exception as e:

#                 print(
#                     f"⚠️ {model_name} failed "
#                     f"(attempt {attempt}/{MAX_RETRIES})"
#                 )

#                 print(
#                     f"Error: {e}"
#                 )

#                 if attempt == MAX_RETRIES:

#                     return None

#                 delay = (
#                     INITIAL_RETRY_DELAY
#                     * (2 ** (attempt - 1))
#                 )

#                 print(
#                     f"⏳ Waiting {delay} seconds..."
#                 )

#                 time.sleep(delay)

#         return None

#     # ------------------------------------------------------
#     # Primary model
#     # ------------------------------------------------------

#     answer = try_model(
#         GEMINI_MODEL
#     )

#     if answer:
#         return answer

#     # ------------------------------------------------------
#     # Fallback model
#     # ------------------------------------------------------

#     print("\n" + "=" * 60)
#     print("PRIMARY MODEL FAILED")
#     print("=" * 60)

#     print(
#         f"Trying fallback model: {FALLBACK_MODEL}"
#     )

#     answer = try_model(
#         FALLBACK_MODEL
#     )

#     if answer:
#         return answer

#     return None


# # ==========================================================
# # NODE 1
# # RETRIEVE FROM QDRANT
# # ==========================================================

# def retrieve_documents(
#     state: GraphState
# ):

#     print("\n" + "=" * 70)
#     print("LANGGRAPH → DOCUMENT RETRIEVAL")
#     print("=" * 70)

#     question = state["question"]

#     conversation_history = (
#         state.get(
#             "conversation_history",
#             []
#         )
#     )

#     # ------------------------------------------------------
#     # Build context-aware retrieval query
#     # ------------------------------------------------------

#     retrieval_query = build_retrieval_query(

#         current_query=question,

#         conversation_history=(
#             conversation_history
#         ),
#     )

#     print(
#         f"\nRetrieval query:\n{retrieval_query}"
#     )

#     # ------------------------------------------------------
#     # Qdrant retrieval
#     # ------------------------------------------------------

#     results = retrieve(
#         retrieval_query
#     )

#     print(
#         f"\n📄 Retrieved {len(results)} chunk(s)"
#     )

#     # ------------------------------------------------------
#     # Extract individual texts
#     # ------------------------------------------------------

#     document_contexts = []

#     for result in results:

#         payload = result.payload or {}

#         text = get_node_text(
#             payload
#         )

#         if text:

#             document_contexts.append(
#                 text
#             )

#     # ------------------------------------------------------
#     # Build formatted context
#     # ------------------------------------------------------

#     context = build_context(
#         results
#     )

#     return {

#         "retrieval_query": retrieval_query,

#         "retrieved_results": results,

#         "document_contexts": document_contexts,

#         "document_context": context,
#     }


# # ==========================================================
# # NODE 2
# # TRY TO ANSWER USING DOCUMENTS
# # ==========================================================

# def answer_from_documents(
#     state: GraphState
# ):

#     print("\n" + "=" * 70)
#     print("LANGGRAPH → CHECKING DOCUMENTS")
#     print("=" * 70)

#     question = state["question"]

#     context = state.get(
#         "document_context",
#         ""
#     )

#     conversation_history = (
#         state.get(
#             "conversation_history",
#             []
#         )
#     )

#     # ------------------------------------------------------
#     # No readable context
#     # ------------------------------------------------------

#     if not context.strip():

#         print(
#             "❌ No readable document context."
#         )

#         return {

#             "document_answer": "NOT_FOUND",

#             "document_found": False,
#         }

#     # ------------------------------------------------------
#     # Conversation history
#     # ------------------------------------------------------

#     history_parts = []

#     for message in conversation_history[-10:]:

#         role = message.get(
#             "role"
#         )

#         content = message.get(
#             "content",
#             ""
#         )

#         if role == "user":

#             history_parts.append(
#                 f"USER: {content}"
#             )

#         elif role == "assistant":

#             history_parts.append(
#                 f"ASSISTANT: {content}"
#             )

#     if history_parts:

#         history_context = "\n".join(
#             history_parts
#         )

#     else:

#         history_context = (
#             "No previous conversation."
#         )

#     # ======================================================
#     # IMPORTANT DOCUMENT ROUTING PROMPT
#     # ======================================================

#     prompt = f"""
# You are the document-answering node in a
# LangGraph RAG system.

# Your ONLY factual source is the retrieved
# document context.

# You must determine whether the documents
# contain enough information to answer the
# CURRENT USER QUESTION.

# ==========================================================
# STRICT RULES
# ==========================================================

# 1. Use ONLY the retrieved document context
#    for factual information.

# 2. Previous conversation may ONLY be used to
#    understand references such as:
#    "it", "this", "that", "he", "she", "they",
#    "the project", etc.

# 3. Do NOT use outside knowledge.

# 4. Do NOT guess.

# 5. Do NOT make assumptions.

# 6. If the retrieved documents contain enough
#    information to answer the question:

#    - Give the answer.
#    - Do NOT mention these instructions.

# 7. If the retrieved documents DO NOT contain
#    enough information:

#    Return EXACTLY:

#    NOT_FOUND

# 8. If the question asks something that clearly
#    cannot be answered from the documents,
#    return:

#    NOT_FOUND

# 9. Do NOT return explanations together with
#    NOT_FOUND.

# 10. If even partially relevant chunks exist but
#     they do not actually contain the answer,
#     return NOT_FOUND.

# ==========================================================
# PREVIOUS CONVERSATION
# ==========================================================

# {history_context}

# ==========================================================
# RETRIEVED DOCUMENT CONTEXT
# ==========================================================

# {context}

# ==========================================================
# CURRENT USER QUESTION
# ==========================================================

# {question}

# ==========================================================
# ANSWER
# ==========================================================
# """

#     answer = generate_with_fallback(
#         prompt
#     )

#     # ------------------------------------------------------
#     # Gemini failed
#     # ------------------------------------------------------

#     if not answer:

#         print(
#             "⚠️ Gemini failed while checking documents."
#         )

#         return {

#             "document_answer": "NOT_FOUND",

#             "document_found": False,
#         }

#     answer = answer.strip()

#     # ------------------------------------------------------
#     # Detect NOT_FOUND
#     # ------------------------------------------------------

#     if answer.upper() == "NOT_FOUND":

#         print(
#             "\n❌ DOCUMENTS CANNOT ANSWER QUESTION"
#         )

#         return {

#             "document_answer": "NOT_FOUND",

#             "document_found": False,
#         }

#     # ------------------------------------------------------
#     # Document answer found
#     # ------------------------------------------------------

#     print(
#         "\n✅ ANSWER FOUND IN DOCUMENTS"
#     )

#     return {

#         "document_answer": answer,

#         "document_found": True,

#         "final_answer": answer,

#         "source": "📄 Provided Documents",
#     }


# # ==========================================================
# # ROUTER
# # ==========================================================

# def route_after_document_check(
#     state: GraphState
# ):

#     if state.get(
#         "document_found",
#         False
#     ):

#         print(
#             "\n➡️ ROUTE: DOCUMENTS"
#         )

#         return "documents"

#     print(
#         "\n➡️ ROUTE: WEB SEARCH"
#     )

#     return "web"


# # ==========================================================
# # NODE 3
# # WEB SEARCH
# # ==========================================================

# def search_web(
#     state: GraphState
# ):

#     print("\n" + "=" * 70)
#     print("LANGGRAPH → WEB SEARCH")
#     print("=" * 70)

#     question = state["question"]

#     print(
#         f"\n🌐 Searching web for:\n{question}"
#     )

#     try:

#         response = tavily_search.invoke(
#             {
#                 "query": question
#             }
#         )

#     except Exception as e:

#         print(
#             f"\n❌ Tavily search failed:"
#         )

#         print(
#             e
#         )

#         return {

#             "web_results": []
#         }

#     # ------------------------------------------------------
#     # Normalize Tavily output
#     # ------------------------------------------------------

#     web_results = []

#     if isinstance(
#         response,
#         dict
#     ):

#         results = response.get(
#             "results",
#             []
#         )

#     elif isinstance(
#         response,
#         list
#     ):

#         results = response

#     else:

#         results = []

#     for item in results:

#         if not isinstance(
#             item,
#             dict
#         ):

#             continue

#         title = item.get(
#             "title",
#             ""
#         )

#         url = item.get(
#             "url",
#             ""
#         )

#         content = item.get(
#             "content",
#             ""
#         )

#         if content:

#             web_results.append({

#                 "title": title,

#                 "url": url,

#                 "content": content,
#             })

#     print(
#         f"\n🌐 Web results found: "
#         f"{len(web_results)}"
#     )

#     for i, result in enumerate(
#         web_results,
#         start=1,
#     ):

#         print(
#             f"\n{i}. {result['title']}"
#         )

#         print(
#             result["url"]
#         )

#     return {

#         "web_results": web_results
#     }


# # ==========================================================
# # NODE 4
# # ANSWER FROM WEB
# # ==========================================================

# def answer_from_web(
#     state: GraphState
# ):

#     print("\n" + "=" * 70)
#     print("LANGGRAPH → GENERATING WEB ANSWER")
#     print("=" * 70)

#     question = state["question"]

#     web_results = state.get(
#         "web_results",
#         []
#     )

#     # ------------------------------------------------------
#     # No web results
#     # ------------------------------------------------------

#     if not web_results:

#         answer = (
#             "I could not find the answer in "
#             "the provided documents or through "
#             "web search."
#         )

#         return {

#             "final_answer": answer,

#             "source": "🌐 Web Search",
#         }

#     # ------------------------------------------------------
#     # Build web context
#     # ------------------------------------------------------

#     web_context_parts = []

#     for i, result in enumerate(
#         web_results,
#         start=1,
#     ):

#         web_context_parts.append(

#             f"""
# WEB SOURCE {i}

# TITLE:
# {result['title']}

# URL:
# {result['url']}

# CONTENT:
# {result['content']}
# """
#         )

#     web_context = "\n".join(
#         web_context_parts
#     )

#     # ======================================================
#     # WEB ANSWERING PROMPT
#     # ======================================================

#     prompt = f"""
# You are a helpful web research assistant.

# The user's question could not be answered
# from the provided documents.

# Use ONLY the web search results below
# to answer the question.

# ==========================================================
# STRICT RULES
# ==========================================================

# 1. Use the web search results as your factual source.

# 2. Do not invent facts.

# 3. Do not use unsupported outside knowledge.

# 4. If multiple sources provide information,
#    synthesize them carefully.

# 5. If the search results still do not contain
#    enough information, say that the information
#    could not be found.

# 6. Keep the answer concise but useful.

# 7. Do not mention these instructions.

# 8. Do not pretend that web information came
#    from the user's documents.

# ==========================================================
# WEB SEARCH RESULTS
# ==========================================================

# {web_context}

# ==========================================================
# USER QUESTION
# ==========================================================

# {question}

# ==========================================================
# ANSWER
# ==========================================================
# """

#     answer = generate_with_fallback(
#         prompt
#     )

#     if not answer:

#         answer = (
#             "I found web search results, but "
#             "the AI service is currently "
#             "unavailable. Please try again."
#         )

#     print(
#         "\n✅ WEB ANSWER GENERATED"
#     )

#     return {

#         "final_answer": answer,

#         "source": "🌐 Web Search",
#     }


# # ==========================================================
# # BUILD LANGGRAPH
# # ==========================================================

# def build_graph():

#     workflow = StateGraph(
#         GraphState
#     )

#     # ------------------------------------------------------
#     # Nodes
#     # ------------------------------------------------------

#     workflow.add_node(
#         "retrieve_documents",
#         retrieve_documents,
#     )

#     workflow.add_node(
#         "answer_from_documents",
#         answer_from_documents,
#     )

#     workflow.add_node(
#         "search_web",
#         search_web,
#     )

#     workflow.add_node(
#         "answer_from_web",
#         answer_from_web,
#     )

#     # ------------------------------------------------------
#     # START
#     # ------------------------------------------------------

#     workflow.add_edge(
#         START,
#         "retrieve_documents",
#     )

#     # ------------------------------------------------------
#     # Retrieval → document answering
#     # ------------------------------------------------------

#     workflow.add_edge(
#         "retrieve_documents",
#         "answer_from_documents",
#     )

#     # ------------------------------------------------------
#     # Conditional routing
#     # ------------------------------------------------------

#     workflow.add_conditional_edges(

#         "answer_from_documents",

#         route_after_document_check,

#         {

#             "documents": END,

#             "web": "search_web",
#         },
#     )

#     # ------------------------------------------------------
#     # Web search → web answer
#     # ------------------------------------------------------

#     workflow.add_edge(
#         "search_web",
#         "answer_from_web",
#     )

#     workflow.add_edge(
#         "answer_from_web",
#         END,
#     )

#     # ------------------------------------------------------
#     # Compile
#     # ------------------------------------------------------

#     return workflow.compile()


# # ==========================================================
# # CREATE GRAPH
# # ==========================================================

# graph = build_graph()


# # ==========================================================
# # PUBLIC FUNCTION
# # ==========================================================

# def run_langgraph_rag(
#     question: str,
#     conversation_history=None,
# ):

#     if conversation_history is None:

#         conversation_history = []

#     initial_state = {

#         "question": question,

#         "conversation_history":
#             conversation_history,

#         "retrieval_query": "",

#         "retrieved_results": [],

#         "document_contexts": [],

#         "document_context": "",

#         "document_answer": "",

#         "document_found": False,

#         "web_results": [],

#         "final_answer": "",

#         "source": "",
#     }

#     result = graph.invoke(
#         initial_state
#     )

#     return {

#         "answer": result.get(
#             "final_answer",
#             ""
#         ),

#         "source": result.get(
#             "source",
#             ""
#         ),

#         "document_found": result.get(
#             "document_found",
#             False
#         ),

#         "document_contexts": result.get(
#             "document_contexts",
#             []
#         ),

#         "web_results": result.get(
#             "web_results",
#             []
#         ),
#     }


# # ==========================================================
# # TEST CHATBOT
# # ==========================================================

# if __name__ == "__main__":

#     print("\n" + "=" * 70)
#     print("🤖 LANGGRAPH RAG CHATBOT")
#     print("=" * 70)

#     print(
#         "\nFlow:"
#     )

#     print(
#         "Qdrant → Documents → Web fallback → Answer"
#     )

#     print(
#         "\nType 'bye', 'goodbye', 'exit', or 'quit' to stop."
#     )

#     conversation_history = []

#     while True:

#         print()

#         question = input(
#             "You: "
#         ).strip()

#         if not question:

#             print(
#                 "Please enter a question."
#             )

#             continue

#         # --------------------------------------------------
#         # Exit
#         # --------------------------------------------------

#         if question.lower() in {
#             "bye",
#             "goodbye",
#             "exit",
#             "quit",
#             "q",
#         }:

#             print(
#                 "\n🤖 Goodbye! 👋"
#             )

#             break

#         # --------------------------------------------------
#         # Run LangGraph
#         # --------------------------------------------------

#         try:

#             result = run_langgraph_rag(

#                 question=question,

#                 conversation_history=(
#                     conversation_history
#                 ),
#             )

#             answer = result["answer"]

#             source = result["source"]

#             # ------------------------------------------------
#             # Save conversation
#             # ------------------------------------------------

#             conversation_history.append({

#                 "role": "user",

#                 "content": question,
#             })

#             conversation_history.append({

#                 "role": "assistant",

#                 "content": answer,
#             })

#             # ------------------------------------------------
#             # Display
#             # ------------------------------------------------

#             print("\n" + "=" * 70)
#             print("🤖 ASSISTANT")
#             print("=" * 70)

#             print(
#                 answer
#             )

#             print(
#                 f"\n{source}"
#             )

#             print("=" * 70)

#         except Exception as e:

#             print(
#                 "\n❌ LangGraph error:"
#             )

#             print(
#                 e
#             )









# import os
# import time

# from typing import TypedDict, List, Optional

# from dotenv import load_dotenv

# from langgraph.graph import (
#     StateGraph,
#     START,
#     END,
# )

# from langchain_tavily import TavilySearch


# # ==========================================================
# # YOUR EXISTING RAG
# # ==========================================================

# from retrieval import (
#     retrieve,
#     build_context,
#     get_node_text,
#     build_retrieval_query,
#     call_gemini,
#     GEMINI_MODEL,
#     FALLBACK_MODEL,
#     MAX_RETRIES,
#     INITIAL_RETRY_DELAY,
# )


# # ==========================================================
# # RUNTIME EVALUATOR
# # ==========================================================

# from runtime_evaluator import (
#     evaluate_runtime_response
# )


# # ==========================================================
# # LOAD ENVIRONMENT
# # ==========================================================

# load_dotenv()


# # ==========================================================
# # TAVILY API KEY
# # ==========================================================

# TAVILY_API_KEY = os.getenv(
#     "TAVILY_API_KEY"
# )


# if not TAVILY_API_KEY:

#     raise RuntimeError(
#         "TAVILY_API_KEY not found in .env file."
#     )


# # ==========================================================
# # TAVILY SEARCH
# # ==========================================================

# tavily_search = TavilySearch(

#     max_results=5,

#     topic="general",
# )


# # ==========================================================
# # LANGGRAPH STATE
# # ==========================================================

# class GraphState(TypedDict):

#     # ------------------------------------------------------
#     # User question
#     # ------------------------------------------------------

#     question: str


#     # ------------------------------------------------------
#     # Conversation history
#     # ------------------------------------------------------

#     conversation_history: List[dict]


#     # ------------------------------------------------------
#     # Retrieval
#     # ------------------------------------------------------

#     retrieval_query: str

#     retrieved_results: list

#     document_contexts: List[str]

#     document_context: str


#     # ------------------------------------------------------
#     # Document answer
#     # ------------------------------------------------------

#     document_answer: str

#     document_found: bool


#     # ------------------------------------------------------
#     # Web search
#     # ------------------------------------------------------

#     web_results: List[dict]


#     # ------------------------------------------------------
#     # Final answer
#     # ------------------------------------------------------

#     final_answer: str

#     source: str


#     # ------------------------------------------------------
#     # Runtime evaluation
#     # ------------------------------------------------------

#     faithfulness: Optional[float]

#     context_precision: Optional[float]

#     answer_relevancy: Optional[float]


# # ==========================================================
# # GEMINI RETRY + FALLBACK
# # ==========================================================

# def generate_with_fallback(
#     prompt: str
# ):

#     """
#     Generate answer using:

#         Primary Gemini model
#                 ↓
#         Retry
#                 ↓
#         Fallback Gemini model
#     """


#     # ======================================================
#     # TRY ONE MODEL
#     # ======================================================

#     def try_model(
#         model_name: str
#     ):

#         for attempt in range(
#             1,
#             MAX_RETRIES + 1
#         ):

#             try:

#                 print(
#                     "\n🤖 Trying "
#                     f"{model_name} "
#                     f"(attempt {attempt}/"
#                     f"{MAX_RETRIES})..."
#                 )


#                 answer = call_gemini(

#                     model=model_name,

#                     prompt=prompt,
#                 )


#                 if answer:

#                     print(
#                         f"✅ {model_name} "
#                         "responded successfully."
#                     )

#                     return answer


#             except Exception as e:

#                 print(
#                     f"\n⚠️ {model_name} failed."
#                 )

#                 print(
#                     f"Error: {e}"
#                 )


#                 # --------------------------------------------------
#                 # Last attempt
#                 # --------------------------------------------------

#                 if attempt == MAX_RETRIES:

#                     return None


#                 delay = (

#                     INITIAL_RETRY_DELAY

#                     * (
#                         2 ** (attempt - 1)
#                     )
#                 )


#                 print(
#                     f"⏳ Retrying in "
#                     f"{delay} seconds..."
#                 )


#                 time.sleep(
#                     delay
#                 )


#         return None


#     # ======================================================
#     # PRIMARY MODEL
#     # ======================================================

#     answer = try_model(
#         GEMINI_MODEL
#     )


#     if answer:

#         return answer


#     # ======================================================
#     # FALLBACK MODEL
#     # ======================================================

#     print(
#         "\n" + "=" * 70
#     )

#     print(
#         "PRIMARY MODEL FAILED"
#     )

#     print(
#         "=" * 70
#     )


#     print(
#         f"Trying fallback model: "
#         f"{FALLBACK_MODEL}"
#     )


#     answer = try_model(
#         FALLBACK_MODEL
#     )


#     if answer:

#         return answer


#     return None


# # ==========================================================
# # NODE 1
# # RETRIEVE DOCUMENTS
# # ==========================================================

# def retrieve_documents(
#     state: GraphState
# ):

#     print(
#         "\n" + "=" * 70
#     )

#     print(
#         "LANGGRAPH → DOCUMENT RETRIEVAL"
#     )

#     print(
#         "=" * 70
#     )


#     question = state[
#         "question"
#     ]


#     conversation_history = state.get(
#         "conversation_history",
#         []
#     )


#     # ======================================================
#     # BUILD RETRIEVAL QUERY
#     # ======================================================

#     retrieval_query = build_retrieval_query(

#         current_query=question,

#         conversation_history=(
#             conversation_history
#         ),
#     )


#     print(
#         "\nRetrieval query:"
#     )

#     print(
#         retrieval_query
#     )


#     # ======================================================
#     # QDRANT RETRIEVAL
#     # ======================================================

#     results = retrieve(
#         retrieval_query
#     )


#     print(
#         "\n📄 Retrieved "
#         f"{len(results)} chunk(s)"
#     )


#     # ======================================================
#     # EXTRACT DOCUMENT TEXT
#     # ======================================================

#     document_contexts = []


#     for result in results:

#         payload = (
#             result.payload
#             or {}
#         )


#         text = get_node_text(
#             payload
#         )


#         if text:

#             document_contexts.append(
#                 text
#             )


#     # ======================================================
#     # BUILD FORMATTED CONTEXT
#     # ======================================================

#     context = build_context(
#         results
#     )


#     return {

#         "retrieval_query":
#             retrieval_query,

#         "retrieved_results":
#             results,

#         "document_contexts":
#             document_contexts,

#         "document_context":
#             context,
#     }


# # ==========================================================
# # NODE 2
# # ANSWER FROM DOCUMENTS
# # ==========================================================

# def answer_from_documents(
#     state: GraphState
# ):

#     print(
#         "\n" + "=" * 70
#     )

#     print(
#         "LANGGRAPH → CHECKING DOCUMENTS"
#     )

#     print(
#         "=" * 70
#     )


#     question = state[
#         "question"
#     ]


#     context = state.get(
#         "document_context",
#         ""
#     )


#     conversation_history = state.get(
#         "conversation_history",
#         []
#     )


#     # ======================================================
#     # NO DOCUMENT CONTEXT
#     # ======================================================

#     if not context.strip():

#         print(
#             "❌ No readable document context."
#         )


#         return {

#             "document_answer":
#                 "NOT_FOUND",

#             "document_found":
#                 False,
#         }


#     # ======================================================
#     # CONVERSATION HISTORY
#     # ======================================================

#     history_parts = []


#     for message in (
#         conversation_history[-10:]
#     ):

#         role = message.get(
#             "role",
#             ""
#         )


#         content = message.get(
#             "content",
#             ""
#         )


#         if role == "user":

#             history_parts.append(
#                 f"USER: {content}"
#             )


#         elif role == "assistant":

#             history_parts.append(
#                 f"ASSISTANT: {content}"
#             )


#     if history_parts:

#         history_context = "\n".join(
#             history_parts
#         )

#     else:

#         history_context = (
#             "No previous conversation."
#         )


#     # ======================================================
#     # DOCUMENT ANSWER PROMPT
#     # ======================================================

#     prompt = f"""
# You are the document-answering node of a
# LangGraph RAG system.

# Your ONLY factual source is the retrieved
# document context.

# Your job is to determine whether the
# CURRENT USER QUESTION can be answered
# using the provided documents.

# ==========================================================
# STRICT RULES
# ==========================================================

# 1. Use ONLY the retrieved document context.

# 2. Do NOT use outside knowledge.

# 3. Do NOT guess.

# 4. Do NOT hallucinate.

# 5. Previous conversation can only be used to
#    understand references such as:

#    "it"
#    "this"
#    "that"
#    "they"
#    "the project"
#    "the document"

# 6. If the documents contain enough information
#    to answer the question, answer normally.

# 7. If the documents DO NOT contain enough
#    information, return EXACTLY:

# NOT_FOUND

# 8. If only a related topic exists but the actual
#    answer is missing, return:

# NOT_FOUND

# 9. Do not write anything before or after
#    NOT_FOUND.

# 10. If you are unsure whether the answer is
#     supported by the documents, return:

# NOT_FOUND

# ==========================================================
# PREVIOUS CONVERSATION
# ==========================================================

# {history_context}

# ==========================================================
# RETRIEVED DOCUMENT CONTEXT
# ==========================================================

# {context}

# ==========================================================
# CURRENT USER QUESTION
# ==========================================================

# {question}

# ==========================================================
# ANSWER
# ==========================================================
# """


#     # ======================================================
#     # GEMINI
#     # ======================================================

#     answer = generate_with_fallback(
#         prompt
#     )


#     # ======================================================
#     # GEMINI FAILURE
#     # ======================================================

#     if not answer:

#         print(
#             "⚠️ Gemini failed."
#         )


#         return {

#             "document_answer":
#                 "NOT_FOUND",

#             "document_found":
#                 False,
#         }


#     answer = answer.strip()


#     # ======================================================
#     # DOCUMENT ANSWER NOT FOUND
#     # ======================================================

#     if answer.upper() == "NOT_FOUND":

#         print(
#             "\n❌ DOCUMENTS CANNOT ANSWER QUESTION"
#         )


#         return {

#             "document_answer":
#                 "NOT_FOUND",

#             "document_found":
#                 False,
#         }


#     # ======================================================
#     # DOCUMENT ANSWER FOUND
#     # ======================================================

#     print(
#         "\n✅ ANSWER FOUND IN DOCUMENTS"
#     )


#     return {

#         "document_answer":
#             answer,

#         "document_found":
#             True,

#         "final_answer":
#             answer,

#         "source":
#             "📄 Provided Documents",
#     }


# # ==========================================================
# # ROUTER
# # ==========================================================

# def route_after_document_check(
#     state: GraphState
# ):

#     if state.get(
#         "document_found",
#         False
#     ):

#         print(
#             "\n➡️ ROUTE: DOCUMENTS"
#         )


#         return "documents"


#     print(
#         "\n➡️ ROUTE: WEB SEARCH"
#     )


#     return "web"


# # ==========================================================
# # NODE 3
# # WEB SEARCH
# # ==========================================================

# def search_web(
#     state: GraphState
# ):

#     print(
#         "\n" + "=" * 70
#     )

#     print(
#         "LANGGRAPH → WEB SEARCH"
#     )

#     print(
#         "=" * 70
#     )


#     question = state[
#         "question"
#     ]


#     print(
#         "\n🌐 Searching web for:"
#     )

#     print(
#         question
#     )


#     try:

#         response = tavily_search.invoke(
#             {
#                 "query": question
#             }
#         )


#     except Exception as e:

#         print(
#             "\n❌ Tavily search failed:"
#         )

#         print(
#             f"{type(e).__name__}: {e}"
#         )


#         return {

#             "web_results": []
#         }


#     # ======================================================
#     # EXTRACT TAVILY RESULTS
#     # ======================================================

#     web_results = []


#     if isinstance(
#         response,
#         dict
#     ):

#         results = response.get(
#             "results",
#             []
#         )


#     elif isinstance(
#         response,
#         list
#     ):

#         results = response


#     else:

#         results = []


#     # ======================================================
#     # NORMALIZE RESULTS
#     # ======================================================

#     for item in results:

#         if not isinstance(
#             item,
#             dict
#         ):

#             continue


#         title = item.get(
#             "title",
#             ""
#         )


#         url = item.get(
#             "url",
#             ""
#         )


#         content = item.get(
#             "content",
#             ""
#         )


#         if content:

#             web_results.append({

#                 "title":
#                     title,

#                 "url":
#                     url,

#                 "content":
#                     content,
#             })


#     print(
#         "\n🌐 Web results found: "
#         f"{len(web_results)}"
#     )


#     # ======================================================
#     # PRINT RESULTS
#     # ======================================================

#     for index, result in enumerate(
#         web_results,
#         start=1
#     ):

#         print(
#             f"\n{index}. "
#             f"{result['title']}"
#         )

#         print(
#             result["url"]
#         )


#     return {

#         "web_results":
#             web_results
#     }


# # ==========================================================
# # NODE 4
# # ANSWER FROM WEB
# # ==========================================================

# def answer_from_web(
#     state: GraphState
# ):

#     print(
#         "\n" + "=" * 70
#     )

#     print(
#         "LANGGRAPH → GENERATING WEB ANSWER"
#     )

#     print(
#         "=" * 70
#     )


#     question = state[
#         "question"
#     ]


#     web_results = state.get(
#         "web_results",
#         []
#     )


#     # ======================================================
#     # NO WEB RESULTS
#     # ======================================================

#     if not web_results:

#         answer = (
#             "I could not find the answer "
#             "in the provided documents or "
#             "through web search."
#         )


#         return {

#             "final_answer":
#                 answer,

#             "source":
#                 "🌐 Web Search",
#         }


#     # ======================================================
#     # BUILD WEB CONTEXT
#     # ======================================================

#     web_context_parts = []


#     for index, result in enumerate(
#         web_results,
#         start=1
#     ):

#         web_context_parts.append(

#             f"""
# WEB SOURCE {index}

# TITLE:
# {result['title']}

# URL:
# {result['url']}

# CONTENT:
# {result['content']}
# """
#         )


#     web_context = "\n".join(
#         web_context_parts
#     )


#     # ======================================================
#     # WEB ANSWERING PROMPT
#     # ======================================================

#     prompt = f"""
# You are a web research assistant.

# The user's question could not be answered
# using the provided documents.

# Use ONLY the web search results below
# to answer the user's question.

# ==========================================================
# RULES
# ==========================================================

# 1. Use the web search results as your
#    factual source.

# 2. Do not invent facts.

# 3. Do not guess.

# 4. Do not pretend web information came
#    from the user's documents.

# 5. If multiple sources contain relevant
#    information, synthesize them.

# 6. If the search results do not contain
#    enough information, clearly say that
#    the information could not be found.

# 7. Keep the answer concise and useful.

# 8. Do not mention these instructions.

# ==========================================================
# WEB SEARCH RESULTS
# ==========================================================

# {web_context}

# ==========================================================
# USER QUESTION
# ==========================================================

# {question}

# ==========================================================
# ANSWER
# ==========================================================
# """


#     # ======================================================
#     # GENERATE WEB ANSWER
#     # ======================================================

#     answer = generate_with_fallback(
#         prompt
#     )


#     if not answer:

#         answer = (
#             "I found web search results, "
#             "but the AI service is currently "
#             "unavailable. Please try again."
#         )


#     print(
#         "\n✅ WEB ANSWER GENERATED"
#     )


#     return {

#         "final_answer":
#             answer,

#         "source":
#             "🌐 Web Search",
#     }


# # ==========================================================
# # NODE 5
# # RUNTIME EVALUATION
# # ==========================================================

# def evaluate_final_answer(
#     state: GraphState
# ):

#     print(
#         "\n" + "=" * 70
#     )

#     print(
#         "LANGGRAPH → RUNTIME EVALUATION"
#     )

#     print(
#         "=" * 70
#     )


#     question = state.get(
#         "question",
#         ""
#     )


#     answer = state.get(
#         "final_answer",
#         ""
#     )


#     source = state.get(
#         "source",
#         ""
#     )


#     # ======================================================
#     # CHOOSE EVALUATION CONTEXT
#     # ======================================================

#     if source == "📄 Provided Documents":

#         # ----------------------------------------------
#         # Document answer
#         # ----------------------------------------------

#         contexts = state.get(
#             "document_contexts",
#             []
#         )


#         print(
#             "\n📄 Evaluating against "
#             "Qdrant document contexts."
#         )


#     else:

#         # ----------------------------------------------
#         # Web answer
#         # ----------------------------------------------

#         web_results = state.get(
#             "web_results",
#             []
#         )


#         contexts = []


#         for result in web_results:

#             content = result.get(
#                 "content",
#                 ""
#             )


#             if content:

#                 contexts.append(
#                     content
#                 )


#         print(
#             "\n🌐 Evaluating against "
#             "web search contexts."
#         )


#     # ======================================================
#     # RUN RAGAS
#     # ======================================================

#     scores = evaluate_runtime_response(

#         question=question,

#         answer=answer,

#         contexts=contexts,
#     )


#     faithfulness = scores.get(
#         "faithfulness"
#     )


#     context_precision = scores.get(
#         "context_precision"
#     )


#     answer_relevancy = scores.get(
#         "answer_relevancy"
#     )


#     # ======================================================
#     # PRINT SCORES
#     # ======================================================

#     print(
#         "\n📊 Runtime Evaluation"
#     )


#     if faithfulness is not None:

#         print(
#             "Faithfulness      : "
#             f"{faithfulness:.4f}"
#         )

#     else:

#         print(
#             "Faithfulness      : N/A"
#         )


#     if context_precision is not None:

#         print(
#             "Context Precision : "
#             f"{context_precision:.4f}"
#         )

#     else:

#         print(
#             "Context Precision : N/A"
#         )


#     if answer_relevancy is not None:

#         print(
#             "Answer Relevancy  : "
#             f"{answer_relevancy:.4f}"
#         )

#     else:

#         print(
#             "Answer Relevancy  : N/A"
#         )


#     # ======================================================
#     # RETURN SCORES INTO LANGGRAPH STATE
#     # ======================================================

#     return {

#         "faithfulness":
#             faithfulness,

#         "context_precision":
#             context_precision,

#         "answer_relevancy":
#             answer_relevancy,
#     }


# # ==========================================================
# # BUILD LANGGRAPH
# # ==========================================================

# def build_graph():

#     workflow = StateGraph(
#         GraphState
#     )


#     # ======================================================
#     # ADD NODES
#     # ======================================================

#     workflow.add_node(

#         "retrieve_documents",

#         retrieve_documents,
#     )


#     workflow.add_node(

#         "answer_from_documents",

#         answer_from_documents,
#     )


#     workflow.add_node(

#         "search_web",

#         search_web,
#     )


#     workflow.add_node(

#         "answer_from_web",

#         answer_from_web,
#     )


#     workflow.add_node(

#         "evaluate_final_answer",

#         evaluate_final_answer,
#     )


#     # ======================================================
#     # START → RETRIEVAL
#     # ======================================================

#     workflow.add_edge(

#         START,

#         "retrieve_documents",
#     )


#     # ======================================================
#     # RETRIEVAL → DOCUMENT ANSWER
#     # ======================================================

#     workflow.add_edge(

#         "retrieve_documents",

#         "answer_from_documents",
#     )


#     # ======================================================
#     # DOCUMENT ANSWER → ROUTER
#     # ======================================================

#     workflow.add_conditional_edges(

#         "answer_from_documents",

#         route_after_document_check,

#         {

#             "documents":
#                 "evaluate_final_answer",

#             "web":
#                 "search_web",
#         },
#     )


#     # ======================================================
#     # WEB SEARCH → WEB ANSWER
#     # ======================================================

#     workflow.add_edge(

#         "search_web",

#         "answer_from_web",
#     )


#     # ======================================================
#     # WEB ANSWER → EVALUATION
#     # ======================================================

#     workflow.add_edge(

#         "answer_from_web",

#         "evaluate_final_answer",
#     )


#     # ======================================================
#     # EVALUATION → END
#     # ======================================================

#     workflow.add_edge(

#         "evaluate_final_answer",

#         END,
#     )


#     # ======================================================
#     # COMPILE
#     # ======================================================

#     return workflow.compile()


# # ==========================================================
# # CREATE GRAPH
# # ==========================================================

# graph = build_graph()


# # ==========================================================
# # PUBLIC FUNCTION
# # ==========================================================

# def run_langgraph_rag(

#     question: str,

#     conversation_history=None,

# ):

#     """
#     Run the complete LangGraph pipeline.

#     Returns:

#         answer
#         source
#         evaluation scores
#         document contexts
#         web results
#     """


#     if conversation_history is None:

#         conversation_history = []


#     # ======================================================
#     # INITIAL STATE
#     # ======================================================

#     initial_state = {

#         "question":
#             question,

#         "conversation_history":
#             conversation_history,

#         "retrieval_query":
#             "",

#         "retrieved_results":
#             [],

#         "document_contexts":
#             [],

#         "document_context":
#             "",

#         "document_answer":
#             "",

#         "document_found":
#             False,

#         "web_results":
#             [],

#         "final_answer":
#             "",

#         "source":
#             "",

#         "faithfulness":
#             None,

#         "context_precision":
#             None,

#         "answer_relevancy":
#             None,
#     }


#     # ======================================================
#     # RUN GRAPH
#     # ======================================================

#     result = graph.invoke(
#         initial_state
#     )


#     # ======================================================
#     # RETURN RESULT
#     # ======================================================

#     return {

#         "answer":
#             result.get(
#                 "final_answer",
#                 ""
#             ),

#         "source":
#             result.get(
#                 "source",
#                 ""
#             ),

#         "document_found":
#             result.get(
#                 "document_found",
#                 False
#             ),

#         "document_contexts":
#             result.get(
#                 "document_contexts",
#                 []
#             ),

#         "web_results":
#             result.get(
#                 "web_results",
#                 []
#             ),

#         "evaluation": {

#             "faithfulness":
#                 result.get(
#                     "faithfulness"
#                 ),

#             "context_precision":
#                 result.get(
#                     "context_precision"
#                 ),

#             "answer_relevancy":
#                 result.get(
#                     "answer_relevancy"
#                 ),
#         },
#     }


# # ==========================================================
# # CHATBOT
# # ==========================================================

# if __name__ == "__main__":

#     print(
#         "\n" + "=" * 70
#     )

#     print(
#         "🤖 LANGGRAPH RAG CHATBOT"
#     )

#     print(
#         "=" * 70
#     )


#     print(
#         "\nPipeline:"
#     )

#     print(
#         "Qdrant → Documents → Web fallback "
#         "→ Runtime Evaluation"
#     )


#     print(
#         "\nEvaluation metrics:"
#     )

#     print(
#         "• Faithfulness"
#     )

#     print(
#         "• Context Precision"
#     )

#     print(
#         "• Answer Relevancy"
#     )


#     print(
#         "\nType 'bye', 'goodbye', 'exit', "
#         "or 'quit' to stop."
#     )


#     # ======================================================
#     # CONVERSATION MEMORY
#     # ======================================================

#     conversation_history = []


#     # ======================================================
#     # CHAT LOOP
#     # ======================================================

#     while True:

#         print()


#         question = input(
#             "You: "
#         ).strip()


#         # ==================================================
#         # EMPTY INPUT
#         # ==================================================

#         if not question:

#             print(
#                 "Please enter a question."
#             )

#             continue


#         # ==================================================
#         # EXIT COMMANDS
#         # ==================================================

#         if question.lower() in {

#             "bye",

#             "goodbye",

#             "exit",

#             "quit",

#             "q",

#         }:

#             print(
#                 "\n🤖 Goodbye! 👋"
#             )

#             break


#         # ==================================================
#         # RUN LANGGRAPH
#         # ==================================================

#         try:

#             result = run_langgraph_rag(

#                 question=question,

#                 conversation_history=(
#                     conversation_history
#                 ),
#             )


#             # ==================================================
#             # EXTRACT RESULT
#             # ==================================================

#             answer = result.get(
#                 "answer",
#                 ""
#             )


#             source = result.get(
#                 "source",
#                 ""
#             )


#             evaluation = result.get(
#                 "evaluation",
#                 {}
#             )


#             # ==================================================
#             # SAVE CONVERSATION
#             # ==================================================

#             conversation_history.append({

#                 "role":
#                     "user",

#                 "content":
#                     question,
#             })


#             conversation_history.append({

#                 "role":
#                     "assistant",

#                 "content":
#                     answer,
#             })


#             # ==================================================
#             # DISPLAY ANSWER
#             # ==================================================

#             print(
#                 "\n" + "=" * 70
#             )


#             print(
#                 "🤖 ASSISTANT"
#             )


#             print(
#                 "=" * 70
#             )


#             print(
#                 answer
#             )


#             # ==================================================
#             # SOURCE
#             # ==================================================

#             print(
#                 f"\n{source}"
#             )


#             # ==================================================
#             # EVALUATION
#             # ==================================================

#             print(
#                 "\n📊 Runtime Evaluation"
#             )


#             faithfulness = evaluation.get(
#                 "faithfulness"
#             )


#             context_precision = evaluation.get(
#                 "context_precision"
#             )


#             answer_relevancy = evaluation.get(
#                 "answer_relevancy"
#             )


#             # --------------------------------------------------
#             # Faithfulness
#             # --------------------------------------------------

#             if faithfulness is not None:

#                 print(
#                     "Faithfulness      : "
#                     f"{faithfulness:.4f}"
#                 )

#             else:

#                 print(
#                     "Faithfulness      : N/A"
#                 )


#             # --------------------------------------------------
#             # Context Precision
#             # --------------------------------------------------

#             if context_precision is not None:

#                 print(
#                     "Context Precision : "
#                     f"{context_precision:.4f}"
#                 )

#             else:

#                 print(
#                     "Context Precision : N/A"
#                 )


#             # --------------------------------------------------
#             # Answer Relevancy
#             # --------------------------------------------------

#             if answer_relevancy is not None:

#                 print(
#                     "Answer Relevancy  : "
#                     f"{answer_relevancy:.4f}"
#                 )

#             else:

#                 print(
#                     "Answer Relevancy  : N/A"
#                 )


#             print(
#                 "=" * 70
#             )


#         except Exception as e:

#             print(
#                 "\n❌ LangGraph error:"
#             )


#             print(
#                 f"{type(e).__name__}: {e}"
#             )











import os
import time

from typing import TypedDict, List, Optional

from dotenv import load_dotenv

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langchain_tavily import TavilySearch


# ==========================================================
# YOUR EXISTING RAG
# ==========================================================

from retrieval import (
    retrieve,
    build_context,
    get_node_text,
    build_retrieval_query,
    call_gemini,
    GEMINI_MODEL,
    FALLBACK_MODEL,
    MAX_RETRIES,
    INITIAL_RETRY_DELAY,
)


# ==========================================================
# REDIS CACHE
# ==========================================================

from redis_cache import (
    get_cached_answer,
    cache_answer,
    is_redis_alive,
    normalize_query,
)


# ==========================================================
# RUNTIME EVALUATOR
# ==========================================================

from runtime_evaluator import (
    evaluate_runtime_response
)


# ==========================================================
# LOAD ENVIRONMENT
# ==========================================================

load_dotenv()


# ==========================================================
# TAVILY API KEY
# ==========================================================

TAVILY_API_KEY = os.getenv(
    "TAVILY_API_KEY"
)


if not TAVILY_API_KEY:

    raise RuntimeError(
        "TAVILY_API_KEY not found in .env file."
    )


# ==========================================================
# TAVILY SEARCH
# ==========================================================

tavily_search = TavilySearch(
    max_results=5,
    topic="general",
)


# ==========================================================
# LANGGRAPH STATE
# ==========================================================

class GraphState(TypedDict):

    # ------------------------------------------------------
    # User question
    # ------------------------------------------------------

    question: str


    # ------------------------------------------------------
    # Conversation history
    # ------------------------------------------------------

    conversation_history: List[dict]


    # ------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------

    retrieval_query: str

    retrieved_results: list

    document_contexts: List[str]

    document_context: str


    # ------------------------------------------------------
    # Document answer
    # ------------------------------------------------------

    document_answer: str

    document_found: bool


    # ------------------------------------------------------
    # Web search
    # ------------------------------------------------------

    web_results: List[dict]


    # ------------------------------------------------------
    # Final answer
    # ------------------------------------------------------

    final_answer: str

    source: str


    # ------------------------------------------------------
    # Runtime evaluation
    # ------------------------------------------------------

    faithfulness: Optional[float]

    context_precision: Optional[float]

    answer_relevancy: Optional[float]


# ==========================================================
# GEMINI RETRY + FALLBACK
# ==========================================================

def generate_with_fallback(
    prompt: str
):

    """
    Generate answer using:

        Primary Gemini model
                ↓
             Retry
                ↓
        Fallback Gemini model
    """

    # ======================================================
    # TRY ONE MODEL
    # ======================================================

    def try_model(
        model_name: str
    ):

        for attempt in range(
            1,
            MAX_RETRIES + 1
        ):

            try:

                print(
                    "\n🤖 Trying "
                    f"{model_name} "
                    f"(attempt {attempt}/"
                    f"{MAX_RETRIES})..."
                )


                answer = call_gemini(
                    model=model_name,
                    prompt=prompt,
                )


                if answer:

                    print(
                        f"✅ {model_name} "
                        "responded successfully."
                    )

                    return answer


            except Exception as e:

                print(
                    f"\n⚠️ {model_name} failed."
                )

                print(
                    f"Error: {e}"
                )


                # --------------------------------------------------
                # Last attempt
                # --------------------------------------------------

                if attempt == MAX_RETRIES:

                    return None


                delay = (
                    INITIAL_RETRY_DELAY
                    * (
                        2 ** (attempt - 1)
                    )
                )


                print(
                    f"⏳ Retrying in "
                    f"{delay} seconds..."
                )


                time.sleep(
                    delay
                )


        return None


    # ======================================================
    # PRIMARY MODEL
    # ======================================================

    answer = try_model(
        GEMINI_MODEL
    )


    if answer:

        return answer


    # ======================================================
    # FALLBACK MODEL
    # ======================================================

    print(
        "\n" + "=" * 70
    )

    print(
        "PRIMARY MODEL FAILED"
    )

    print(
        "=" * 70
    )


    print(
        f"Trying fallback model: "
        f"{FALLBACK_MODEL}"
    )


    answer = try_model(
        FALLBACK_MODEL
    )


    if answer:

        return answer


    return None


# ==========================================================
# NODE 1
# RETRIEVE DOCUMENTS
# ==========================================================

def retrieve_documents(
    state: GraphState
):

    print(
        "\n" + "=" * 70
    )

    print(
        "LANGGRAPH → DOCUMENT RETRIEVAL"
    )

    print(
        "=" * 70
    )


    question = state[
        "question"
    ]


    conversation_history = state.get(
        "conversation_history",
        []
    )


    # ======================================================
    # BUILD RETRIEVAL QUERY
    # ======================================================

    retrieval_query = build_retrieval_query(

        current_query=question,

        conversation_history=(
            conversation_history
        ),

    )


    print(
        "\nRetrieval query:"
    )

    print(
        retrieval_query
    )


    # ======================================================
    # QDRANT RETRIEVAL
    # ======================================================

    results = retrieve(
        retrieval_query
    )


    print(
        "\n📄 Retrieved "
        f"{len(results)} chunk(s)"
    )


    # ======================================================
    # EXTRACT DOCUMENT TEXT
    # ======================================================

    document_contexts = []


    for result in results:

        payload = (
            result.payload
            or {}
        )


        text = get_node_text(
            payload
        )


        if text:

            document_contexts.append(
                text
            )


    # ======================================================
    # BUILD FORMATTED CONTEXT
    # ======================================================

    context = build_context(
        results
    )


    return {

        "retrieval_query":
            retrieval_query,

        "retrieved_results":
            results,

        "document_contexts":
            document_contexts,

        "document_context":
            context,

    }


# ==========================================================
# NODE 2
# ANSWER FROM DOCUMENTS
# ==========================================================

def answer_from_documents(
    state: GraphState
):

    print(
        "\n" + "=" * 70
    )

    print(
        "LANGGRAPH → CHECKING DOCUMENTS"
    )

    print(
        "=" * 70
    )


    question = state[
        "question"
    ]


    context = state.get(
        "document_context",
        ""
    )


    conversation_history = state.get(
        "conversation_history",
        []
    )


    # ======================================================
    # NO DOCUMENT CONTEXT
    # ======================================================

    if not context.strip():

        print(
            "❌ No readable document context."
        )


        return {

            "document_answer":
                "NOT_FOUND",

            "document_found":
                False,

        }


    # ======================================================
    # CONVERSATION HISTORY
    # ======================================================

    history_parts = []


    for message in (
        conversation_history[-10:]
    ):

        role = message.get(
            "role",
            ""
        )


        content = message.get(
            "content",
            ""
        )


        if role == "user":

            history_parts.append(
                f"USER: {content}"
            )


        elif role == "assistant":

            history_parts.append(
                f"ASSISTANT: {content}"
            )


    if history_parts:

        history_context = "\n".join(
            history_parts
        )

    else:

        history_context = (
            "No previous conversation."
        )


    # ======================================================
    # DOCUMENT ANSWER PROMPT
    # ======================================================

    prompt = f"""
You are the document-answering node of a
LangGraph RAG system.

Your ONLY factual source is the retrieved
document context.

Your job is to determine whether the
CURRENT USER QUESTION can be answered
using the provided documents.

==========================================================
STRICT RULES
==========================================================

1. Use ONLY the retrieved document context.

2. Do NOT use outside knowledge.

3. Do NOT guess.

4. Do NOT hallucinate.

5. Previous conversation can only be used to
   understand references such as:

   "it"
   "this"
   "that"
   "they"
   "the project"
   "the document"

6. If the documents contain enough information
   to answer the question, answer normally.

7. If the documents DO NOT contain enough
   information, return EXACTLY:

NOT_FOUND

8. If only a related topic exists but the actual
   answer is missing, return:

NOT_FOUND

9. Do not write anything before or after
   NOT_FOUND.

10. If you are unsure whether the answer is
    supported by the documents, return:

NOT_FOUND

==========================================================
PREVIOUS CONVERSATION
==========================================================

{history_context}

==========================================================
RETRIEVED DOCUMENT CONTEXT
==========================================================

{context}

==========================================================
CURRENT USER QUESTION
==========================================================

{question}

==========================================================
ANSWER
==========================================================
"""


    # ======================================================
    # GEMINI
    # ======================================================

    answer = generate_with_fallback(
        prompt
    )


    # ======================================================
    # GEMINI FAILURE
    # ======================================================

    if not answer:

        print(
            "⚠️ Gemini failed."
        )


        return {

            "document_answer":
                "NOT_FOUND",

            "document_found":
                False,

        }


    answer = answer.strip()


    # ======================================================
    # DOCUMENT ANSWER NOT FOUND
    # ======================================================

    if answer.upper() == "NOT_FOUND":

        print(
            "\n❌ DOCUMENTS CANNOT ANSWER QUESTION"
        )


        return {

            "document_answer":
                "NOT_FOUND",

            "document_found":
                False,

        }


    # ======================================================
    # DOCUMENT ANSWER FOUND
    # ======================================================

    print(
        "\n✅ ANSWER FOUND IN DOCUMENTS"
    )


    return {

        "document_answer":
            answer,

        "document_found":
            True,

        "final_answer":
            answer,

        "source":
            "📄 Provided Documents",

    }


# ==========================================================
# ROUTER
# ==========================================================

def route_after_document_check(
    state: GraphState
):

    if state.get(
        "document_found",
        False
    ):

        print(
            "\n➡️ ROUTE: DOCUMENTS"
        )


        return "documents"


    print(
        "\n➡️ ROUTE: WEB SEARCH"
    )


    return "web"


# ==========================================================
# NODE 3
# WEB SEARCH
# ==========================================================

def search_web(
    state: GraphState
):

    print(
        "\n" + "=" * 70
    )

    print(
        "LANGGRAPH → WEB SEARCH"
    )

    print(
        "=" * 70
    )


    question = state[
        "question"
    ]


    print(
        "\n🌐 Searching web for:"
    )

    print(
        question
    )


    try:

        response = tavily_search.invoke(
            {
                "query": question
            }
        )


    except Exception as e:

        print(
            "\n❌ Tavily search failed:"
        )

        print(
            f"{type(e).__name__}: {e}"
        )


        return {

            "web_results": []

        }


    # ======================================================
    # EXTRACT TAVILY RESULTS
    # ======================================================

    web_results = []


    if isinstance(
        response,
        dict
    ):

        results = response.get(
            "results",
            []
        )


    elif isinstance(
        response,
        list
    ):

        results = response


    else:

        results = []


    # ======================================================
    # NORMALIZE RESULTS
    # ======================================================

    for item in results:

        if not isinstance(
            item,
            dict
        ):

            continue


        title = item.get(
            "title",
            ""
        )


        url = item.get(
            "url",
            ""
        )


        content = item.get(
            "content",
            ""
        )


        if content:

            web_results.append({

                "title":
                    title,

                "url":
                    url,

                "content":
                    content,

            })


    print(
        "\n🌐 Web results found: "
        f"{len(web_results)}"
    )


    # ======================================================
    # PRINT RESULTS
    # ======================================================

    for index, result in enumerate(
        web_results,
        start=1
    ):

        print(
            f"\n{index}. "
            f"{result['title']}"
        )

        print(
            result["url"]
        )


    return {

        "web_results":
            web_results

    }


# ==========================================================
# NODE 4
# ANSWER FROM WEB
# ==========================================================

def answer_from_web(
    state: GraphState
):

    print(
        "\n" + "=" * 70
    )

    print(
        "LANGGRAPH → GENERATING WEB ANSWER"
    )

    print(
        "=" * 70
    )


    question = state[
        "question"
    ]


    web_results = state.get(
        "web_results",
        []
    )


    # ======================================================
    # NO WEB RESULTS
    # ======================================================

    if not web_results:

        answer = (
            "I could not find the answer "
            "in the provided documents or "
            "through web search."
        )


        return {

            "final_answer":
                answer,

            "source":
                "🌐 Web Search",

        }


    # ======================================================
    # BUILD WEB CONTEXT
    # ======================================================

    web_context_parts = []


    for index, result in enumerate(
        web_results,
        start=1
    ):

        web_context_parts.append(
            f"""
WEB SOURCE {index}

TITLE:
{result['title']}

URL:
{result['url']}

CONTENT:
{result['content']}
"""
        )


    web_context = "\n".join(
        web_context_parts
    )


    # ======================================================
    # WEB ANSWERING PROMPT
    # ======================================================

    prompt = f"""
You are a web research assistant.

The user's question could not be answered
using the provided documents.

Use ONLY the web search results below
to answer the user's question.

==========================================================
RULES
==========================================================

1. Use the web search results as your
   factual source.

2. Do not invent facts.

3. Do not guess.

4. Do not pretend web information came
   from the user's documents.

5. If multiple sources contain relevant
   information, synthesize them.

6. If the search results do not contain
   enough information, clearly say that
   the information could not be found.

7. Keep the answer concise and useful.

8. Do not mention these instructions.

==========================================================
WEB SEARCH RESULTS
==========================================================

{web_context}

==========================================================
USER QUESTION
==========================================================

{question}

==========================================================
ANSWER
==========================================================
"""


    # ======================================================
    # GENERATE WEB ANSWER
    # ======================================================

    answer = generate_with_fallback(
        prompt
    )


    if not answer:

        answer = (
            "I found web search results, "
            "but the AI service is currently "
            "unavailable. Please try again."
        )


    print(
        "\n✅ WEB ANSWER GENERATED"
    )


    return {

        "final_answer":
            answer,

        "source":
            "🌐 Web Search",

    }


# ==========================================================
# NODE 5
# RUNTIME EVALUATION
# ==========================================================

def evaluate_final_answer(
    state: GraphState
):

    print(
        "\n" + "=" * 70
    )

    print(
        "LANGGRAPH → RUNTIME EVALUATION"
    )

    print(
        "=" * 70
    )


    question = state.get(
        "question",
        ""
    )


    answer = state.get(
        "final_answer",
        ""
    )


    source = state.get(
        "source",
        ""
    )


    # ======================================================
    # CHOOSE EVALUATION CONTEXT
    # ======================================================

    if source == "📄 Provided Documents":

        # ----------------------------------------------
        # Document answer
        # ----------------------------------------------

        contexts = state.get(
            "document_contexts",
            []
        )


        print(
            "\n📄 Evaluating against "
            "Qdrant document contexts."
        )


    else:

        # ----------------------------------------------
        # Web answer
        # ----------------------------------------------

        web_results = state.get(
            "web_results",
            []
        )


        contexts = []


        for result in web_results:

            content = result.get(
                "content",
                ""
            )


            if content:

                contexts.append(
                    content
                )


        print(
            "\n🌐 Evaluating against "
            "web search contexts."
        )


    # ======================================================
    # RUN RAGAS
    # ======================================================

    scores = evaluate_runtime_response(

        question=question,

        answer=answer,

        contexts=contexts,

    )


    faithfulness = scores.get(
        "faithfulness"
    )


    context_precision = scores.get(
        "context_precision"
    )


    answer_relevancy = scores.get(
        "answer_relevancy"
    )


    # ======================================================
    # PRINT SCORES
    # ======================================================

    print(
        "\n📊 Runtime Evaluation"
    )


    if faithfulness is not None:

        print(
            "Faithfulness      : "
            f"{faithfulness:.4f}"
        )

    else:

        print(
            "Faithfulness      : N/A"
        )


    if context_precision is not None:

        print(
            "Context Precision : "
            f"{context_precision:.4f}"
        )

    else:

        print(
            "Context Precision : N/A"
        )


    if answer_relevancy is not None:

        print(
            "Answer Relevancy  : "
            f"{answer_relevancy:.4f}"
        )

    else:

        print(
            "Answer Relevancy  : N/A"
        )


    # ======================================================
    # RETURN SCORES INTO LANGGRAPH STATE
    # ======================================================

    return {

        "faithfulness":
            faithfulness,

        "context_precision":
            context_precision,

        "answer_relevancy":
            answer_relevancy,

    }


# ==========================================================
# BUILD LANGGRAPH
# ==========================================================

def build_graph():

    workflow = StateGraph(
        GraphState
    )


    # ======================================================
    # ADD NODES
    # ======================================================

    workflow.add_node(
        "retrieve_documents",
        retrieve_documents,
    )


    workflow.add_node(
        "answer_from_documents",
        answer_from_documents,
    )


    workflow.add_node(
        "search_web",
        search_web,
    )


    workflow.add_node(
        "answer_from_web",
        answer_from_web,
    )


    workflow.add_node(
        "evaluate_final_answer",
        evaluate_final_answer,
    )


    # ======================================================
    # START → RETRIEVAL
    # ======================================================

    workflow.add_edge(

        START,

        "retrieve_documents",

    )


    # ======================================================
    # RETRIEVAL → DOCUMENT ANSWER
    # ======================================================

    workflow.add_edge(

        "retrieve_documents",

        "answer_from_documents",

    )


    # ======================================================
    # DOCUMENT ANSWER → ROUTER
    # ======================================================

    workflow.add_conditional_edges(

        "answer_from_documents",

        route_after_document_check,

        {

            "documents":
                "evaluate_final_answer",

            "web":
                "search_web",

        },

    )


    # ======================================================
    # WEB SEARCH → WEB ANSWER
    # ======================================================

    workflow.add_edge(

        "search_web",

        "answer_from_web",

    )


    # ======================================================
    # WEB ANSWER → EVALUATION
    # ======================================================

    workflow.add_edge(

        "answer_from_web",

        "evaluate_final_answer",

    )


    # ======================================================
    # EVALUATION → END
    # ======================================================

    workflow.add_edge(

        "evaluate_final_answer",

        END,

    )


    # ======================================================
    # COMPILE
    # ======================================================

    return workflow.compile()


# ==========================================================
# CREATE GRAPH
# ==========================================================

graph = build_graph()


# ==========================================================
# PUBLIC FUNCTION
# ==========================================================

def run_langgraph_rag(
    question: str,
    conversation_history=None,
):

    """
    Run the complete LangGraph RAG pipeline
    with Redis caching.

    Pipeline:

        User Question
             ↓
        Redis Cache
          ↙      ↘
       HIT       MISS
        ↓          ↓
     Answer     LangGraph
                  ↓
               Qdrant
                  ↓
          Document Answer
             ↙       ↘
          Found    NOT_FOUND
            ↓          ↓
        Evaluation   Tavily
                       ↓
                  Web Answer
                       ↓
                   Evaluation
                       ↓
                  Save Redis
                       ↓
                    Answer

    Redis cache key uses ONLY the current
    user question, not the conversation-expanded
    retrieval query.
    """

    if conversation_history is None:

        conversation_history = []


    # ======================================================
    # REDIS CACHE CHECK
    # ======================================================

    print(
        "\n" + "=" * 70
    )

    print(
        "CHECKING REDIS CACHE"
    )

    print(
        "=" * 70
    )


    redis_available = False


    try:

        redis_available = is_redis_alive()


    except Exception as e:

        print(
            "⚠️ Redis health check failed:"
        )

        print(
            f"{type(e).__name__}: {e}"
        )


        redis_available = False


    # ======================================================
    # REDIS AVAILABLE
    # ======================================================

    if redis_available:

        print(
            "✅ Redis is connected"
        )


        try:

            # ------------------------------------------------
            # IMPORTANT:
            # Use the ORIGINAL question for caching.
            #
            # Do NOT use build_retrieval_query() here because
            # that query contains conversation history and can
            # change between turns.
            # ------------------------------------------------

            cache_key = normalize_query(
                question
            )


            cached_answer = get_cached_answer(
                question
            )


            # ==================================================
            # CACHE HIT
            # ==================================================

            if cached_answer:

                print(
                    "\n🟢 REDIS CACHE HIT"
                )

                print(
                    f"Cache key: {cache_key}"
                )

                print(
                    "\n⚡ Returning cached answer."
                )

                print(
                    "Qdrant will NOT be called."
                )

                print(
                    "Gemini will NOT be called."
                )

                print(
                    "Tavily will NOT be called."
                )

                print(
                    "Runtime evaluator will NOT be called."
                )


                return {

                    "answer":
                        cached_answer,

                    "source":
                        "💾 Redis Cache",

                    "document_found":
                        False,

                    "document_contexts":
                        [],

                    "web_results":
                        [],

                    "evaluation": {

                        "faithfulness":
                            None,

                        "context_precision":
                            None,

                        "answer_relevancy":
                            None,

                    },

                }


            # ==================================================
            # CACHE MISS
            # ==================================================

            print(
                "\n🔴 REDIS CACHE MISS"
            )

            print(
                f"Cache key: {cache_key}"
            )

            print(
                "Starting LangGraph..."
            )


        except Exception as e:

            print(
                "\n⚠️ Redis cache lookup failed:"
            )

            print(
                f"{type(e).__name__}: {e}"
            )

            print(
                "Continuing without Redis cache."
            )


    else:

        print(
            "⚠️ Redis is unavailable."
        )

        print(
            "Continuing without Redis cache."
        )


    # ======================================================
    # INITIAL STATE
    # ======================================================

    initial_state = {

        "question":
            question,

        "conversation_history":
            conversation_history,

        "retrieval_query":
            "",

        "retrieved_results":
            [],

        "document_contexts":
            [],

        "document_context":
            "",

        "document_answer":
            "",

        "document_found":
            False,

        "web_results":
            [],

        "final_answer":
            "",

        "source":
            "",

        "faithfulness":
            None,

        "context_precision":
            None,

        "answer_relevancy":
            None,

    }


    # ======================================================
    # RUN LANGGRAPH
    # ======================================================

    result = graph.invoke(
        initial_state
    )


    # ======================================================
    # EXTRACT FINAL ANSWER
    # ======================================================

    answer = result.get(
        "final_answer",
        ""
    )


    source = result.get(
        "source",
        ""
    )


    # ======================================================
    # SAVE ANSWER TO REDIS
    # ======================================================

    if redis_available and answer:

        try:

            cache_answer(
                question,
                answer
            )


            print(
                "\n🟢 ANSWER SAVED TO REDIS CACHE"
            )


        except Exception as e:

            print(
                "\n⚠️ Could not save answer "
                "to Redis cache:"
            )

            print(
                f"{type(e).__name__}: {e}"
            )


    # ======================================================
    # RETURN RESULT
    # ======================================================

    return {

        "answer":
            answer,

        "source":
            source,

        "document_found":
            result.get(
                "document_found",
                False
            ),

        "document_contexts":
            result.get(
                "document_contexts",
                []
            ),

        "web_results":
            result.get(
                "web_results",
                []
            ),

        "evaluation": {

            "faithfulness":
                result.get(
                    "faithfulness"
                ),

            "context_precision":
                result.get(
                    "context_precision"
                ),

            "answer_relevancy":
                result.get(
                    "answer_relevancy"
                ),

        },

    }


# ==========================================================
# CHATBOT
# ==========================================================

if __name__ == "__main__":

    print(
        "\n" + "=" * 70
    )

    print(
        "🤖 LANGGRAPH RAG CHATBOT"
    )

    print(
        "=" * 70
    )


    print(
        "\nPipeline:"
    )

    print(
        "Redis Cache → "
        "Qdrant → Documents → "
        "Web fallback → Runtime Evaluation → "
        "Redis Cache"
    )


    print(
        "\nEvaluation metrics:"
    )

    print(
        "• Faithfulness"
    )

    print(
        "• Context Precision"
    )

    print(
        "• Answer Relevancy"
    )


    print(
        "\nType 'bye', 'goodbye', 'exit', "
        "'quit', or 'q' to stop."
    )


    # ======================================================
    # CONVERSATION MEMORY
    # ======================================================

    conversation_history = []


    # ======================================================
    # CHAT LOOP
    # ======================================================

    while True:

        print()


        question = input(
            "You: "
        ).strip()


        # ==================================================
        # EMPTY INPUT
        # ==================================================

        if not question:

            print(
                "Please enter a question."
            )

            continue


        # ==================================================
        # EXIT COMMANDS
        # ==================================================

        if question.lower() in {

            "bye",

            "goodbye",

            "exit",

            "quit",

            "q",

        }:

            print(
                "\n🤖 Goodbye! 👋"
            )

            break


        # ==================================================
        # RUN LANGGRAPH
        # ==================================================

        try:

            result = run_langgraph_rag(

                question=question,

                conversation_history=(
                    conversation_history
                ),

            )


            # ==================================================
            # EXTRACT RESULT
            # ==================================================

            answer = result.get(
                "answer",
                ""
            )


            source = result.get(
                "source",
                ""
            )


            evaluation = result.get(
                "evaluation",
                {}
            )


            # ==================================================
            # SAVE CONVERSATION
            # ==================================================

            conversation_history.append({

                "role":
                    "user",

                "content":
                    question,

            })


            conversation_history.append({

                "role":
                    "assistant",

                "content":
                    answer,

            })


            # ==================================================
            # DISPLAY ANSWER
            # ==================================================

            print(
                "\n" + "=" * 70
            )


            print(
                "🤖 ASSISTANT"
            )


            print(
                "=" * 70
            )


            print(
                answer
            )


            # ==================================================
            # SOURCE
            # ==================================================

            print(
                f"\n{source}"
            )


            # ==================================================
            # EVALUATION
            # ==================================================

            print(
                "\n📊 Runtime Evaluation"
            )


            faithfulness = evaluation.get(
                "faithfulness"
            )


            context_precision = evaluation.get(
                "context_precision"
            )


            answer_relevancy = evaluation.get(
                "answer_relevancy"
            )


            # --------------------------------------------------
            # Faithfulness
            # --------------------------------------------------

            if faithfulness is not None:

                print(
                    "Faithfulness      : "
                    f"{faithfulness:.4f}"
                )

            else:

                print(
                    "Faithfulness      : N/A"
                )


            # --------------------------------------------------
            # Context Precision
            # --------------------------------------------------

            if context_precision is not None:

                print(
                    "Context Precision : "
                    f"{context_precision:.4f}"
                )

            else:

                print(
                    "Context Precision : N/A"
                )


            # --------------------------------------------------
            # Answer Relevancy
            # --------------------------------------------------

            if answer_relevancy is not None:

                print(
                    "Answer Relevancy  : "
                    f"{answer_relevancy:.4f}"
                )

            else:

                print(
                    "Answer Relevancy  : N/A"
                )


            print(
                "=" * 70
            )


        except Exception as e:

            print(
                "\n❌ LangGraph error:"
            )


            print(
                f"{type(e).__name__}: {e}"
            )