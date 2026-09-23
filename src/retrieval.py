# # # # # # import chromadb

# # # # # # from llama_index.core import VectorStoreIndex
# # # # # # from llama_index.vector_stores.chroma import ChromaVectorStore
# # # # # # from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# # # # # # import os
# # # # # # from google import genai
# # # # # # from dotenv import load_dotenv


# # # # # # #Configure Gemini
# # # # # # load_dotenv()
# # # # # # client = genai.Client(
# # # # # #     api_key=os.getenv("GOOGLE_API_KEY")
# # # # # # )


# # # # # # #connecting to existing data
# # # # # # db = chromadb.PersistentClient(path="./chroma_db")
# # # # # # collection = db.get_or_create_collection("documents")


# # # # # # #create vector store
# # # # # # vector_store = ChromaVectorStore(
# # # # # #     chroma_collection=collection
# # # # # # )


# # # # # # #Load the same embedding model
# # # # # # embed_model = HuggingFaceEmbedding(
# # # # # #     model_name="BAAI/bge-small-en-v1.5"
# # # # # # )


# # # # # # #Rebuild the index from ChromaDB
# # # # # # '''  We're not embedding the PDFs again.
# # # # # # We're simply telling LlamaIndex:
# # # # # # "Use the vectors already stored in Chroma.  '''
# # # # # # index = VectorStoreIndex.from_vector_store(
# # # # # #     vector_store=vector_store,
# # # # # #     embed_model=embed_model
# # # # # # )


# # # # # # #creating a retriever
# # # # # # retriever = index.as_retriever(
# # # # # #     similarity_top_k=3              #provide the top 3 chunks whenever a question is asked
# # # # # # )


# # # # # # #ask a question
# # # # # # question = input("What is your question?")  #"What programming languages does Devanshi know?"
# # # # # # #Retrieve
# # # # # # nodes = retriever.retrieve(question)
# # # # # # #filtering the nodes
# # # # # # nodes = [node for node in nodes if node.score > 0.30]
# # # # # # # Stop if nothing relevant remains
# # # # # # if not nodes:
# # # # # #     print("No relevant information found.")
# # # # # #     exit()


# # # # # # #building the context
# # # # # # context = "\n\n".join(
# # # # # #     [node.text for node in nodes]
# # # # # # )


# # # # # # #printing retrieved chunks
# # # # # # print(f"Retrieved {len(nodes)} chunks\n")

# # # # # # # for i, node in enumerate(nodes, start=1):
# # # # # # #     print("=" * 50)
# # # # # # #     print(f"Chunk {i}")
# # # # # # #     print("=" * 50)

# # # # # # #     print(node.text[:500])
# # # # # # #     print()


# # # # # # for i, node in enumerate(nodes, start=1):
# # # # # #     print("=" * 60)
# # # # # #     print(f"NODE {i}")

# # # # # #     print("Similarity:", node.score)
# # # # # #     print("Characters:", len(node.text))
# # # # # #     print("Words:", len(node.text.split()))

# # # # # #     print(node.text)
# # # # # # # llm.complete(prompt)


# # # # # # #Create the prompt
# # # # # # prompt = f"""
# # # # # # You are a helpful AI chatbot.

# # # # # # Answer ONLY using the provided context.

# # # # # # Context:
# # # # # # {context}

# # # # # # Question:
# # # # # # {question}

# # # # # # If the answer cannot be found in the context, reply exactly:

# # # # # # Based on the provided context, no answer can be found.
# # # # # # """


# # # # # # #get response from gemini
# # # # # # response = client.models.generate_content(
# # # # # #     model="gemini-3.6-flash",
# # # # # #     contents=prompt
# # # # # # )
# # # # # # print(response.text)

# # # # # # #print the answer
# # # # # # # print("\n" + "=" * 60)
# # # # # # # print("ANSWER")
# # # # # # # print("=" * 60)

# # # # # # # print(response.text)



# # # # # import os
# # # # # import chromadb

# # # # # from dotenv import load_dotenv
# # # # # from google import genai

# # # # # from llama_index.core import VectorStoreIndex
# # # # # from llama_index.vector_stores.chroma import ChromaVectorStore
# # # # # from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# # # # # from embedding import embed_model

# # # # # from redis_cache import (
# # # # #     get_cached_answer,
# # # # #     cache_answer,
# # # # #     is_redis_alive
# # # # # )


# # # # # # -------------------------------------------------------
# # # # # # Configure Gemini
# # # # # # -------------------------------------------------------

# # # # # load_dotenv()

# # # # # client = genai.Client(
# # # # #     api_key=os.getenv("GOOGLE_API_KEY")
# # # # # )

# # # # # # -------------------------------------------------------
# # # # # # Connect to ChromaDB
# # # # # # -------------------------------------------------------

# # # # # db = chromadb.PersistentClient(path="./chroma_db")

# # # # # collection = db.get_or_create_collection("documents")

# # # # # vector_store = ChromaVectorStore(
# # # # #     chroma_collection=collection
# # # # # )

# # # # # # -------------------------------------------------------
# # # # # # Embedding Model
# # # # # # -------------------------------------------------------

# # # # # embed_model = HuggingFaceEmbedding(
# # # # #     model_name="BAAI/bge-small-en-v1.5"
# # # # # )

# # # # # # -------------------------------------------------------
# # # # # # Load Index
# # # # # # -------------------------------------------------------

# # # # # index = VectorStoreIndex.from_vector_store(
# # # # #     vector_store=vector_store,
# # # # #     embed_model=embed_model
# # # # # )

# # # # # # -------------------------------------------------------
# # # # # # Retriever
# # # # # # -------------------------------------------------------

# # # # # retriever = index.as_retriever(
# # # # #     similarity_top_k=3
# # # # # )

# # # # # # ============================================
# # # # # # Conversation Memory
# # # # # # ============================================

# # # # # conversation_history = []

# # # # # # -------------------------------------------------------
# # # # # # User Question
# # # # # # -------------------------------------------------------

# # # # # while True:

# # # # #     question = input("\nYou: ")

# # # # # # ----------------------------
# # # # # # Check Redis Cache
# # # # # # ----------------------------

# # # # #     cached_answer = get_cached_answer(question)

# # # # #     if cached_answer:

# # # # #         print("\n⚡ CACHE HIT")
# # # # #         print("=" * 80)
# # # # #         print(cached_answer)

# # # # #         conversation_history.append({
# # # # #             "role": "User",
# # # # #             "content": question
# # # # #     })

# # # # #         conversation_history.append({
# # # # #             "role": "Assistant",
# # # # #             "content": cached_answer
# # # # #     })

# # # # #         continue

# # # # #     if question.lower() in ["exit", "quit", "bye"]:
# # # # #         print("\nGoodbye!")
# # # # #         break

# # # # # # -------------------------------------------------------
# # # # # # Retrieve
# # # # # # -------------------------------------------------------

# # # # #     nodes = retriever.retrieve(question)

# # # # # # Filter weak matches
# # # # #     nodes = [node for node in nodes if node.score > 0.30]

# # # # #     if not nodes:
# # # # #         print("\nNo relevant information found.")
# # # # #         exit()

# # # # # # -------------------------------------------------------
# # # # # # Retrieved Chunks
# # # # # # -------------------------------------------------------

# # # # #     print(f"\nRetrieved {len(nodes)} chunks\n")

# # # # #     for i, node in enumerate(nodes, start=1):

# # # # #         print("=" * 80)
# # # # #         print(f"NODE {i}")
# # # # #     # print("=" * 80)

# # # # #         print("Metadata:", node.metadata)

# # # # #         print(f"Similarity : {node.score:.4f}")
# # # # #         print(f"Characters : {len(node.text)}")
# # # # #         print(f"Words      : {len(node.text.split())}")

# # # # #         print("-" * 80)
# # # # #         print(node.text)
# # # # #         print()

# # # # # # -------------------------------------------------------
# # # # # # Build Context
# # # # # # -------------------------------------------------------

# # # # #     context = "\n\n".join(
# # # # #         node.text for node in nodes
# # # # #     )


# # # # # #Build conversation history
# # # # #     history = ""

# # # # #     for message in conversation_history:
# # # # #         history += f"{message['role']}: {message['content']}\n"

# # # # # # -------------------------------------------------------
# # # # # # Prompt
# # # # # # -------------------------------------------------------

# # # # #     prompt = f"""
# # # # #     You are a helpful AI chatbot.

# # # # #     You are having an ongoing conversation with the user.

# # # # #     Previous Conversation:
# # # # #     {history}

# # # # #     Relevant Context:
# # # # #     {context}

# # # # #     Current Question:
# # # # #     {question}

# # # # #     Instructions:

# # # # #     1. Use the previous conversation whenever needed.
# # # # #     2. Use the retrieved context to answer accurately.
# # # # #     3. If the current question refers to earlier messages using words like
# # # # #         "she", "he", "it", "that", "those", "his", "her", etc.,
# # # # #         resolve them using the conversation history.
# # # # #     4. If the answer is not present in the retrieved context,
# # # # #         reply exactly:

# # # # #     Based on the provided context, no answer can be found.
# # # # # """

# # # # # #Save the user's question
# # # # #     conversation_history.append(
# # # # #         {
# # # # #             "role": "User",
# # # # #             "content": question
# # # # #         }
# # # # # )

# # # # # # -------------------------------------------------------
# # # # # # Gemini
# # # # # # -------------------------------------------------------

# # # # #     response = client.models.generate_content(
# # # # #         model="gemini-3.6-flash",
# # # # #         contents=prompt
# # # # #     )

# # # # #     cache_answer(
# # # # #         question,
# # # # #         response.text
# # # # # )

# # # # # #to grow memory
# # # # #     conversation_history.append(
# # # # #     {
# # # # #         "role": "Assistant",
# # # # #         "content": response.text
# # # # #     }
# # # # # )


# # # # # # -------------------------------------------------------
# # # # # # Final Answer
# # # # # # -------------------------------------------------------

# # # # #     print("\n" + "=" * 80)
# # # # #     print("ANSWER")
# # # # #     print("=" * 80)
# # # # #     print(response.text)


# # # # # #added last
# # # # #     print("\n" + "=" * 60)
# # # # #     print("📚 SOURCES")
# # # # #     print("=" * 60)

# # # # #     shown = set()

# # # # #     for i, node in enumerate(nodes, start=1):

# # # # #         filename = node.metadata.get("filename", "Unknown")
# # # # #         filetype = node.metadata.get("type", "Unknown")

# # # # #     # Avoid showing duplicate sources
# # # # #         if filename in shown:
# # # # #             continue

# # # # #         shown.add(filename)

# # # # #         print(f"{len(shown)}. {filename}")
# # # # #         print(f"   Type       : {filetype}")
# # # # #         print(f"   Similarity : {node.score:.4f}")
# # # # #         print()


# # # # # #Keep only the last 10 messages
# # # # #         if len(conversation_history) > 10:

# # # # #             conversation_history = conversation_history[-10:]




# # # # import os

# # # # from qdrant_client import QdrantClient

# # # # from embedding import embed_model


# # # # # ==========================================================
# # # # # CONFIGURATION
# # # # # ==========================================================

# # # # QDRANT_PATH = "./qdrant_db"
# # # # COLLECTION_NAME = "documents"

# # # # TOP_K = 3


# # # # # ==========================================================
# # # # # CONNECT TO QDRANT
# # # # # ==========================================================

# # # # print("Connecting to Qdrant...")

# # # # qdrant_client = QdrantClient(
# # # #     path=QDRANT_PATH
# # # # )

# # # # print("✅ Qdrant connected")


# # # # # ==========================================================
# # # # # CHECK COLLECTION
# # # # # ==========================================================

# # # # collections = qdrant_client.get_collections()

# # # # collection_names = [
# # # #     collection.name
# # # #     for collection in collections.collections
# # # # ]

# # # # if COLLECTION_NAME not in collection_names:

# # # #     print(
# # # #         f"❌ Collection '{COLLECTION_NAME}' does not exist."
# # # #     )

# # # #     qdrant_client.close()

# # # #     raise SystemExit(1)


# # # # print(f"✅ Collection '{COLLECTION_NAME}' found")


# # # # # ==========================================================
# # # # # RETRIEVAL FUNCTION
# # # # # ==========================================================

# # # # def retrieve(query: str, top_k: int = TOP_K):

# # # #     print("\n" + "=" * 60)
# # # #     print("USER QUERY")
# # # #     print("=" * 60)

# # # #     print(query)

# # # #     # ------------------------------------------------------
# # # #     # Convert query into embedding
# # # #     # ------------------------------------------------------

# # # #     query_embedding = embed_model.get_text_embedding(
# # # #         query
# # # #     )

# # # #     print(
# # # #         f"\nQuery embedding dimension: "
# # # #         f"{len(query_embedding)}"
# # # #     )

# # # #     # ------------------------------------------------------
# # # #     # Search Qdrant
# # # #     # ------------------------------------------------------

# # # #     results = qdrant_client.query_points(
# # # #         collection_name=COLLECTION_NAME,
# # # #         query=query_embedding,
# # # #         limit=top_k,
# # # #         with_payload=True,
# # # #     )

# # # #     return results.points


# # # # # ==========================================================
# # # # # TEST RETRIEVAL
# # # # # ==========================================================

# # # # if __name__ == "__main__":

# # # #     query = input(
# # # #         "\nAsk a question about your documents: "
# # # #     )

# # # #     results = retrieve(query)

# # # #     print("\n" + "=" * 60)
# # # #     print("RETRIEVED CHUNKS")
# # # #     print("=" * 60)

# # # #     if not results:

# # # #         print("❌ No results found.")

# # # #     else:

# # # #         for i, result in enumerate(results, start=1):

# # # #             print("\n" + "-" * 60)
# # # #             print(f"RESULT {i}")
# # # #             print("-" * 60)

# # # #             print(f"Score: {result.score}")

# # # #             payload = result.payload or {}

# # # #             print(
# # # #                 f"File: "
# # # #                 f"{payload.get('filename', 'Unknown')}"
# # # #             )

# # # #             print(
# # # #                 f"Extension: "
# # # #                 f"{payload.get('extension', 'Unknown')}"
# # # #             )

# # # #             print("\nText:")

# # # #             print(
# # # #                 payload.get(
# # # #                     "text",
# # # #                     payload.get(
# # # #                         "content",
# # # #                         "No text found in payload."
# # # #                     )
# # # #                 )
# # # #             )

# # # #     print("\n" + "=" * 60)
# # # #     print("RETRIEVAL TEST COMPLETED")
# # # #     print("=" * 60)

# # # #     qdrant_client.close()





# # # # import json

# # # # from qdrant_client import QdrantClient

# # # # from embedding import embed_model


# # # # # ==========================================================
# # # # # CONFIGURATION
# # # # # ==========================================================

# # # # QDRANT_PATH = "./qdrant_db"
# # # # COLLECTION_NAME = "documents"

# # # # TOP_K = 3


# # # # # ==========================================================
# # # # # CONNECT TO QDRANT
# # # # # ==========================================================

# # # # print("Connecting to Qdrant...")

# # # # qdrant_client = QdrantClient(
# # # #     path=QDRANT_PATH
# # # # )

# # # # print("✅ Qdrant connected")


# # # # # ==========================================================
# # # # # CHECK COLLECTION
# # # # # ==========================================================

# # # # collections = qdrant_client.get_collections()

# # # # collection_names = [
# # # #     collection.name
# # # #     for collection in collections.collections
# # # # ]

# # # # if COLLECTION_NAME not in collection_names:

# # # #     print(
# # # #         f"❌ Collection '{COLLECTION_NAME}' does not exist."
# # # #     )

# # # #     qdrant_client.close()

# # # #     raise SystemExit(1)


# # # # print(f"✅ Collection '{COLLECTION_NAME}' found")


# # # # # ==========================================================
# # # # # EXTRACT TEXT FROM PAYLOAD
# # # # # ==========================================================

# # # # def get_node_text(payload):
# # # #     """
# # # #     Extract the original text from a LlamaIndex payload.
# # # #     """

# # # #     if not payload:
# # # #         return "No payload found."

# # # #     # ------------------------------------------------------
# # # #     # Case 1: LlamaIndex stores node as JSON
# # # #     # ------------------------------------------------------

# # # #     node_content = payload.get("_node_content")

# # # #     if node_content:

# # # #         try:

# # # #             node_data = json.loads(node_content)

# # # #             text = node_data.get("text")

# # # #             if text:
# # # #                 return text

# # # #         except Exception:
# # # #             pass

# # # #     # ------------------------------------------------------
# # # #     # Case 2: Direct text/content fields
# # # #     # ------------------------------------------------------

# # # #     if payload.get("text"):
# # # #         return payload["text"]

# # # #     if payload.get("content"):
# # # #         return payload["content"]

# # # #     return "No text found in payload."


# # # # # ==========================================================
# # # # # RETRIEVAL FUNCTION
# # # # # ==========================================================

# # # # def retrieve(query: str, top_k: int = TOP_K):

# # # #     print("\n" + "=" * 60)
# # # #     print("USER QUERY")
# # # #     print("=" * 60)

# # # #     print(query)

# # # #     # ------------------------------------------------------
# # # #     # Convert query into embedding
# # # #     # ------------------------------------------------------

# # # #     query_embedding = embed_model.get_text_embedding(
# # # #         query
# # # #     )

# # # #     print(
# # # #         f"\nQuery embedding dimension: "
# # # #         f"{len(query_embedding)}"
# # # #     )

# # # #     # ------------------------------------------------------
# # # #     # Search Qdrant
# # # #     # ------------------------------------------------------

# # # #     results = qdrant_client.query_points(
# # # #         collection_name=COLLECTION_NAME,
# # # #         query=query_embedding,
# # # #         limit=top_k,
# # # #         with_payload=True,
# # # #     )

# # # #     return results.points


# # # # # ==========================================================
# # # # # TEST RETRIEVAL
# # # # # ==========================================================

# # # # if __name__ == "__main__":

# # # #     query = input(
# # # #         "\nAsk a question about your documents: "
# # # #     )

# # # #     results = retrieve(query)

# # # #     print("\n" + "=" * 60)
# # # #     print("RETRIEVED CHUNKS")
# # # #     print("=" * 60)

# # # #     if not results:

# # # #         print("❌ No results found.")

# # # #     else:

# # # #         for i, result in enumerate(results, start=1):

# # # #             print("\n" + "-" * 60)
# # # #             print(f"RESULT {i}")
# # # #             print("-" * 60)

# # # #             print(f"Score: {result.score}")

# # # #             payload = result.payload or {}

# # # #             print(
# # # #                 f"File: "
# # # #                 f"{payload.get('filename', 'Unknown')}"
# # # #             )

# # # #             print(
# # # #                 f"Extension: "
# # # #                 f"{payload.get('extension', 'Unknown')}"
# # # #             )

# # # #             print("\nText:")

# # # #             print(
# # # #                 get_node_text(payload)
# # # #             )

# # # #     print("\n" + "=" * 60)
# # # #     print("RETRIEVAL TEST COMPLETED")
# # # #     print("=" * 60)

# # # #     qdrant_client.close()





# # # import os
# # # import json

# # # from dotenv import load_dotenv
# # # from google import genai
# # # from qdrant_client import QdrantClient

# # # from embedding import embed_model


# # # # ==========================================================
# # # # CONFIGURATION
# # # # ==========================================================

# # # QDRANT_PATH = "./qdrant_db"
# # # COLLECTION_NAME = "documents"

# # # TOP_K = 3

# # # GEMINI_MODEL = "gemini-3.6-flash"


# # # # ==========================================================
# # # # CONFIGURE GEMINI
# # # # ==========================================================

# # # load_dotenv()

# # # api_key = os.getenv("GOOGLE_API_KEY")

# # # if not api_key:
# # #     raise RuntimeError(
# # #         "GOOGLE_API_KEY not found in environment variables."
# # #     )

# # # gemini_client = genai.Client(
# # #     api_key=api_key
# # # )


# # # # ==========================================================
# # # # CONNECT TO QDRANT
# # # # ==========================================================

# # # print("Connecting to Qdrant...")

# # # qdrant_client = QdrantClient(
# # #     path=QDRANT_PATH
# # # )

# # # print("✅ Qdrant connected")


# # # # ==========================================================
# # # # CHECK COLLECTION
# # # # ==========================================================

# # # collections = qdrant_client.get_collections()

# # # collection_names = [
# # #     collection.name
# # #     for collection in collections.collections
# # # ]

# # # if COLLECTION_NAME not in collection_names:

# # #     qdrant_client.close()

# # #     raise RuntimeError(
# # #         f"Collection '{COLLECTION_NAME}' does not exist."
# # #     )

# # # print(f"✅ Collection '{COLLECTION_NAME}' found")


# # # # ==========================================================
# # # # EXTRACT TEXT FROM QDRANT PAYLOAD
# # # # ==========================================================

# # # def get_node_text(payload):
# # #     """
# # #     Extract original chunk text from a LlamaIndex payload.
# # #     """

# # #     if not payload:
# # #         return ""

# # #     # ------------------------------------------------------
# # #     # LlamaIndex stores TextNode as JSON in _node_content
# # #     # ------------------------------------------------------

# # #     node_content = payload.get("_node_content")

# # #     if node_content:

# # #         try:

# # #             node_data = json.loads(node_content)

# # #             text = node_data.get("text")

# # #             if text:
# # #                 return text.strip()

# # #         except (json.JSONDecodeError, TypeError):

# # #             pass

# # #     # ------------------------------------------------------
# # #     # Fallback: direct text field
# # #     # ------------------------------------------------------

# # #     text = payload.get("text")

# # #     if text:
# # #         return str(text).strip()

# # #     # ------------------------------------------------------
# # #     # Fallback: content field
# # #     # ------------------------------------------------------

# # #     content = payload.get("content")

# # #     if content:
# # #         return str(content).strip()

# # #     return ""


# # # # ==========================================================
# # # # RETRIEVE DOCUMENT CHUNKS
# # # # ==========================================================

# # # def retrieve(query: str, top_k: int = TOP_K):

# # #     print("\n" + "=" * 60)
# # #     print("USER QUERY")
# # #     print("=" * 60)

# # #     print(query)

# # #     # ------------------------------------------------------
# # #     # Embed user query
# # #     # ------------------------------------------------------

# # #     query_embedding = embed_model.get_text_embedding(query)

# # #     print(
# # #         f"\nQuery embedding dimension: "
# # #         f"{len(query_embedding)}"
# # #     )

# # #     # ------------------------------------------------------
# # #     # Search Qdrant
# # #     # ------------------------------------------------------

# # #     results = qdrant_client.query_points(
# # #         collection_name=COLLECTION_NAME,
# # #         query=query_embedding,
# # #         limit=top_k,
# # #         with_payload=True,
# # #         with_vectors=False,
# # #     )

# # #     return results.points


# # # # ==========================================================
# # # # BUILD CONTEXT FOR GEMINI
# # # # ==========================================================

# # # def build_context(results):

# # #     context_parts = []

# # #     for i, result in enumerate(results, start=1):

# # #         payload = result.payload or {}

# # #         filename = payload.get(
# # #             "filename",
# # #             "Unknown file"
# # #         )

# # #         text = get_node_text(payload)

# # #         if not text:
# # #             continue

# # #         context_parts.append(
# # #             f"""
# # # SOURCE {i}
# # # FILE: {filename}
# # # RELEVANCE SCORE: {result.score}

# # # CONTENT:
# # # {text}
# # # """
# # #         )

# # #     return "\n".join(context_parts)


# # # # ==========================================================
# # # # ASK GEMINI
# # # # ==========================================================

# # # def generate_answer(query, context):

# # #     if not context.strip():

# # #         return (
# # #             "I could not find any readable text in the "
# # #             "retrieved documents."
# # #         )

# # #     prompt = f"""
# # # You are a helpful document question-answering assistant.

# # # Answer the user's question using ONLY the information
# # # provided in the document context below.

# # # Do not use outside knowledge.

# # # If the answer is not present in the context, clearly say:
# # # "I could not find this information in the provided documents."

# # # Give a clear and concise explanation.

# # # DOCUMENT CONTEXT:
# # # {context}

# # # USER QUESTION:
# # # {query}

# # # ANSWER:
# # # """

# # #     response = gemini_client.models.generate_content(
# # #         model=GEMINI_MODEL,
# # #         contents=prompt,
# # #     )

# # #     return response.text


# # # # ==========================================================
# # # # MAIN RAG PIPELINE
# # # # ==========================================================

# # # if __name__ == "__main__":

# # #     try:

# # #         query = input(
# # #             "\nAsk a question about your documents: "
# # #         ).strip()

# # #         if not query:

# # #             print("❌ Please enter a question.")

# # #             raise SystemExit(1)

# # #         # --------------------------------------------------
# # #         # STEP 1 — Retrieval
# # #         # --------------------------------------------------

# # #         results = retrieve(query)

# # #         print("\n" + "=" * 60)
# # #         print("RETRIEVED CHUNKS")
# # #         print("=" * 60)

# # #         if not results:

# # #             print("❌ No results found.")

# # #             raise SystemExit(0)

# # #         # --------------------------------------------------
# # #         # STEP 2 — Display retrieved chunks
# # #         # --------------------------------------------------

# # #         for i, result in enumerate(results, start=1):

# # #             print("\n" + "-" * 60)
# # #             print(f"RESULT {i}")
# # #             print("-" * 60)

# # #             print(f"Score: {result.score}")

# # #             payload = result.payload or {}

# # #             print(
# # #                 f"File: "
# # #                 f"{payload.get('filename', 'Unknown')}"
# # #             )

# # #             print(
# # #                 f"Extension: "
# # #                 f"{payload.get('extension', 'Unknown')}"
# # #             )

# # #             text = get_node_text(payload)

# # #             print("\nText:")

# # #             if text:
# # #                 print(text)
# # #             else:
# # #                 print("⚠️ No text found.")

# # #         # --------------------------------------------------
# # #         # STEP 3 — Build context
# # #         # --------------------------------------------------

# # #         context = build_context(results)

# # #         print("\n" + "=" * 60)
# # #         print("GENERATING ANSWER")
# # #         print("=" * 60)

# # #         # --------------------------------------------------
# # #         # STEP 4 — Send context + query to Gemini
# # #         # --------------------------------------------------

# # #         answer = generate_answer(
# # #             query=query,
# # #             context=context,
# # #         )

# # #         # --------------------------------------------------
# # #         # STEP 5 — Final answer
# # #         # --------------------------------------------------

# # #         print("\n" + "=" * 60)
# # #         print("FINAL ANSWER")
# # #         print("=" * 60)

# # #         print(answer)

# # #         print("\n" + "=" * 60)
# # #         print("RAG PIPELINE COMPLETED")
# # #         print("=" * 60)

# # #     finally:

# # #         qdrant_client.close()






# # # import os
# # # import json
# # # import time

# # # from dotenv import load_dotenv
# # # from google import genai
# # # from qdrant_client import QdrantClient

# # # from embedding import embed_model


# # # # ==========================================================
# # # # CONFIGURATION
# # # # ==========================================================

# # # QDRANT_PATH = "./qdrant_db"
# # # COLLECTION_NAME = "documents"

# # # TOP_K = 3

# # # # Primary model
# # # GEMINI_MODEL = "gemini-3.6-flash"

# # # # Fallback model
# # # FALLBACK_MODEL = "gemini-3.5-flash"

# # # # Number of attempts for each model
# # # MAX_RETRIES = 3

# # # # Exponential backoff:
# # # # retry 1 -> 2 sec
# # # # retry 2 -> 4 sec
# # # # retry 3 -> 8 sec
# # # INITIAL_RETRY_DELAY = 2


# # # # ==========================================================
# # # # CONFIGURE GEMINI
# # # # ==========================================================

# # # load_dotenv()

# # # api_key = os.getenv("GOOGLE_API_KEY")

# # # if not api_key:
# # #     raise RuntimeError(
# # #         "GOOGLE_API_KEY not found in environment variables."
# # #     )

# # # gemini_client = genai.Client(
# # #     api_key=api_key
# # # )


# # # # ==========================================================
# # # # CONNECT TO QDRANT
# # # # ==========================================================

# # # print("Connecting to Qdrant...")

# # # qdrant_client = QdrantClient(
# # #     path=QDRANT_PATH
# # # )

# # # print("✅ Qdrant connected")


# # # # ==========================================================
# # # # CHECK COLLECTION
# # # # ==========================================================

# # # collections = qdrant_client.get_collections()

# # # collection_names = [
# # #     collection.name
# # #     for collection in collections.collections
# # # ]

# # # if COLLECTION_NAME not in collection_names:

# # #     qdrant_client.close()

# # #     raise RuntimeError(
# # #         f"Collection '{COLLECTION_NAME}' does not exist."
# # #     )

# # # print(f"✅ Collection '{COLLECTION_NAME}' found")


# # # # ==========================================================
# # # # EXTRACT TEXT FROM QDRANT PAYLOAD
# # # # ==========================================================

# # # def get_node_text(payload):
# # #     """
# # #     Extract original chunk text from a LlamaIndex payload.
# # #     """

# # #     if not payload:
# # #         return ""

# # #     # ------------------------------------------------------
# # #     # Case 1:
# # #     # LlamaIndex stores TextNode as JSON
# # #     # inside "_node_content"
# # #     # ------------------------------------------------------

# # #     node_content = payload.get("_node_content")

# # #     if node_content:

# # #         try:

# # #             node_data = json.loads(node_content)

# # #             text = node_data.get("text")

# # #             if text:
# # #                 return text.strip()

# # #         except (json.JSONDecodeError, TypeError):

# # #             pass

# # #     # ------------------------------------------------------
# # #     # Case 2:
# # #     # Direct text field
# # #     # ------------------------------------------------------

# # #     text = payload.get("text")

# # #     if text:
# # #         return str(text).strip()

# # #     # ------------------------------------------------------
# # #     # Case 3:
# # #     # Direct content field
# # #     # ------------------------------------------------------

# # #     content = payload.get("content")

# # #     if content:
# # #         return str(content).strip()

# # #     return ""


# # # # ==========================================================
# # # # RETRIEVE DOCUMENT CHUNKS
# # # # ==========================================================

# # # def retrieve(query: str, top_k: int = TOP_K):

# # #     print("\n" + "=" * 60)
# # #     print("USER QUERY")
# # #     print("=" * 60)

# # #     print(query)

# # #     # ------------------------------------------------------
# # #     # Embed user query
# # #     # ------------------------------------------------------

# # #     query_embedding = embed_model.get_text_embedding(
# # #         query
# # #     )

# # #     print(
# # #         f"\nQuery embedding dimension: "
# # #         f"{len(query_embedding)}"
# # #     )

# # #     # ------------------------------------------------------
# # #     # Search Qdrant
# # #     # ------------------------------------------------------

# # #     results = qdrant_client.query_points(
# # #         collection_name=COLLECTION_NAME,
# # #         query=query_embedding,
# # #         limit=top_k,
# # #         with_payload=True,
# # #         with_vectors=False,
# # #     )

# # #     return results.points


# # # # ==========================================================
# # # # BUILD CONTEXT FOR GEMINI
# # # # ==========================================================

# # # def build_context(results):

# # #     context_parts = []

# # #     source_number = 1

# # #     for result in results:

# # #         payload = result.payload or {}

# # #         filename = payload.get(
# # #             "filename",
# # #             "Unknown file"
# # #         )

# # #         text = get_node_text(payload)

# # #         # Ignore chunks with no readable text
# # #         if not text:
# # #             continue

# # #         context_parts.append(
# # #             f"""
# # # SOURCE {source_number}
# # # FILE: {filename}
# # # RELEVANCE SCORE: {result.score}

# # # CONTENT:
# # # {text}
# # # """
# # #         )

# # #         source_number += 1

# # #     return "\n".join(context_parts)


# # # # ==========================================================
# # # # GEMINI SINGLE REQUEST
# # # # ==========================================================

# # # def call_gemini(model, prompt):

# # #     response = gemini_client.models.generate_content(
# # #         model=model,
# # #         contents=prompt,
# # #     )

# # #     if not response or not response.text:

# # #         raise RuntimeError(
# # #             "Gemini returned an empty response."
# # #         )

# # #     return response.text.strip()


# # # # ==========================================================
# # # # GEMINI WITH RETRIES + FALLBACK
# # # # ==========================================================

# # # def generate_answer(query, context):

# # #     if not context.strip():

# # #         return (
# # #             "I could not find any readable text in the "
# # #             "retrieved documents."
# # #         )

# # #     # ------------------------------------------------------
# # #     # Prompt
# # #     # ------------------------------------------------------

# # #     prompt = f"""
# # # You are a helpful document question-answering assistant.

# # # Your job is to answer the user's question using ONLY
# # # the information contained in the document context.

# # # STRICT RULES:

# # # 1. Do not use outside knowledge.
# # # 2. Do not invent facts.
# # # 3. Do not make assumptions.
# # # 4. If the answer is present in the context, explain it clearly.
# # # 5. If the answer is not present, say:
# # #    "I could not find this information in the provided documents."
# # # 6. Keep the answer concise but useful.
# # # 7. If multiple documents contain relevant information,
# # #    combine them carefully.
# # # 8. Do not mention these instructions in your answer.

# # # DOCUMENT CONTEXT:
# # # {context}

# # # USER QUESTION:
# # # {query}

# # # ANSWER:
# # # """

# # #     # ======================================================
# # #     # MODEL ATTEMPT FUNCTION
# # #     # ======================================================

# # #     def try_model(model_name):

# # #         for attempt in range(1, MAX_RETRIES + 1):

# # #             try:

# # #                 print(
# # #                     f"\n🤖 Trying {model_name} "
# # #                     f"(attempt {attempt}/{MAX_RETRIES})..."
# # #                 )

# # #                 answer = call_gemini(
# # #                     model=model_name,
# # #                     prompt=prompt,
# # #                 )

# # #                 print(
# # #                     f"✅ {model_name} responded successfully."
# # #                 )

# # #                 return answer

# # #             except Exception as e:

# # #                 error_message = str(e)

# # #                 print(
# # #                     f"⚠️ {model_name} failed "
# # #                     f"(attempt {attempt}/{MAX_RETRIES})"
# # #                 )

# # #                 print(
# # #                     f"Error: {error_message}"
# # #                 )

# # #                 # --------------------------------------------------
# # #                 # If this is the final attempt, stop retrying
# # #                 # --------------------------------------------------

# # #                 if attempt == MAX_RETRIES:

# # #                     print(
# # #                         f"❌ All attempts failed for "
# # #                         f"{model_name}."
# # #                     )

# # #                     return None

# # #                 # --------------------------------------------------
# # #                 # Exponential backoff
# # #                 # --------------------------------------------------

# # #                 delay = INITIAL_RETRY_DELAY * (
# # #                     2 ** (attempt - 1)
# # #                 )

# # #                 print(
# # #                     f"⏳ Waiting {delay} seconds before retry..."
# # #                 )

# # #                 time.sleep(delay)

# # #         return None

# # #     # ======================================================
# # #     # PRIMARY MODEL
# # #     # ======================================================

# # #     answer = try_model(
# # #         GEMINI_MODEL
# # #     )

# # #     if answer:

# # #         return answer

# # #     # ======================================================
# # #     # FALLBACK MODEL
# # #     # ======================================================

# # #     print("\n" + "=" * 60)
# # #     print("PRIMARY MODEL FAILED")
# # #     print("=" * 60)

# # #     print(
# # #         f"Trying fallback model: {FALLBACK_MODEL}"
# # #     )

# # #     answer = try_model(
# # #         FALLBACK_MODEL
# # #     )

# # #     if answer:

# # #         return answer

# # #     # ======================================================
# # #     # BOTH MODELS FAILED
# # #     # ======================================================

# # #     return (
# # #         "I retrieved the relevant information from your "
# # #         "documents, but the Gemini service is currently "
# # #         "unavailable. Please try the question again in "
# # #         "a moment."
# # #     )


# # # # ==========================================================
# # # # MAIN RAG PIPELINE
# # # # ==========================================================

# # # if __name__ == "__main__":

# # #     try:

# # #         # --------------------------------------------------
# # #         # USER QUERY
# # #         # --------------------------------------------------

# # #         query = input(
# # #             "\nAsk a question about your documents: "
# # #         ).strip()

# # #         if not query:

# # #             print("❌ Please enter a question.")

# # #             raise SystemExit(1)

# # #         # --------------------------------------------------
# # #         # STEP 1 — RETRIEVAL
# # #         # --------------------------------------------------

# # #         results = retrieve(query)

# # #         print("\n" + "=" * 60)
# # #         print("RETRIEVED CHUNKS")
# # #         print("=" * 60)

# # #         if not results:

# # #             print("❌ No results found.")

# # #             raise SystemExit(0)

# # #         # --------------------------------------------------
# # #         # STEP 2 — DISPLAY RETRIEVED CHUNKS
# # #         # --------------------------------------------------

# # #         for i, result in enumerate(
# # #             results,
# # #             start=1
# # #         ):

# # #             print("\n" + "-" * 60)
# # #             print(f"RESULT {i}")
# # #             print("-" * 60)

# # #             print(
# # #                 f"Score: {result.score}"
# # #             )

# # #             payload = result.payload or {}

# # #             print(
# # #                 f"File: "
# # #                 f"{payload.get('filename', 'Unknown')}"
# # #             )

# # #             print(
# # #                 f"Extension: "
# # #                 f"{payload.get('extension', 'Unknown')}"
# # #             )

# # #             text = get_node_text(payload)

# # #             print("\nText:")

# # #             if text:

# # #                 print(text)

# # #             else:

# # #                 print("⚠️ No text found.")

# # #         # --------------------------------------------------
# # #         # STEP 3 — BUILD CONTEXT
# # #         # --------------------------------------------------

# # #         context = build_context(results)

# # #         if not context.strip():

# # #             print(
# # #                 "\n❌ Retrieved chunks contain no readable text."
# # #             )

# # #             raise SystemExit(0)

# # #         # --------------------------------------------------
# # #         # STEP 4 — GENERATE ANSWER
# # #         # --------------------------------------------------

# # #         print("\n" + "=" * 60)
# # #         print("GENERATING ANSWER")
# # #         print("=" * 60)

# # #         answer = generate_answer(
# # #             query=query,
# # #             context=context,
# # #         )

# # #         # --------------------------------------------------
# # #         # STEP 5 — FINAL ANSWER
# # #         # --------------------------------------------------

# # #         print("\n" + "=" * 60)
# # #         print("FINAL ANSWER")
# # #         print("=" * 60)

# # #         print(answer)

# # #         print("\n" + "=" * 60)
# # #         print("RAG PIPELINE COMPLETED")
# # #         print("=" * 60)

# # #     finally:

# # #         qdrant_client.close()








# # import os
# # import json
# # import time

# # from dotenv import load_dotenv
# # from google import genai
# # from qdrant_client import QdrantClient

# # from embedding import embed_model

# # from redis_cache import (
# #     get_cached_answer,
# #     cache_answer,
# #     is_redis_alive
# # )


# # # ==========================================================
# # # CONFIGURATION
# # # ==========================================================

# # QDRANT_PATH = "./qdrant_db"

# # COLLECTION_NAME = "documents"

# # TOP_K = 3


# # # ==========================================================
# # # GEMINI CONFIGURATION
# # # ==========================================================

# # # Primary model
# # GEMINI_MODEL = "gemini-3.6-flash"

# # # Fallback model
# # FALLBACK_MODEL = "gemini-3.5-flash"

# # # Number of attempts for each model
# # MAX_RETRIES = 3

# # # Retry delays:
# # #
# # # Attempt 1 fails -> wait 2 sec
# # # Attempt 2 fails -> wait 4 sec
# # # Attempt 3 fails -> stop
# # #
# # INITIAL_RETRY_DELAY = 2


# # # ==========================================================
# # # CONFIGURE GEMINI
# # # ==========================================================

# # load_dotenv()

# # api_key = os.getenv("GOOGLE_API_KEY")

# # if not api_key:

# #     raise RuntimeError(
# #         "GOOGLE_API_KEY not found in environment variables."
# #     )


# # gemini_client = genai.Client(
# #     api_key=api_key
# # )


# # # ==========================================================
# # # CONNECT TO QDRANT
# # # ==========================================================

# # print("Connecting to Qdrant...")

# # qdrant_client = QdrantClient(
# #     path=QDRANT_PATH
# # )

# # print("✅ Qdrant connected")


# # # ==========================================================
# # # CHECK COLLECTION
# # # ==========================================================

# # collections = qdrant_client.get_collections()

# # collection_names = [
# #     collection.name
# #     for collection in collections.collections
# # ]


# # if COLLECTION_NAME not in collection_names:

# #     qdrant_client.close()

# #     raise RuntimeError(
# #         f"Collection '{COLLECTION_NAME}' does not exist."
# #     )


# # print(
# #     f"✅ Collection '{COLLECTION_NAME}' found"
# # )


# # # ==========================================================
# # # EXTRACT TEXT FROM QDRANT PAYLOAD
# # # ==========================================================

# # def get_node_text(payload):
# #     """
# #     Extract original chunk text from a LlamaIndex payload.

# #     LlamaIndex stores TextNode information inside
# #     the '_node_content' field as JSON.
# #     """

# #     if not payload:

# #         return ""


# #     # ------------------------------------------------------
# #     # CASE 1
# #     # LlamaIndex TextNode stored as JSON
# #     # ------------------------------------------------------

# #     node_content = payload.get(
# #         "_node_content"
# #     )


# #     if node_content:

# #         try:

# #             node_data = json.loads(
# #                 node_content
# #             )

# #             text = node_data.get(
# #                 "text"
# #             )

# #             if text:

# #                 return text.strip()

# #         except (
# #             json.JSONDecodeError,
# #             TypeError,
# #         ):

# #             pass


# #     # ------------------------------------------------------
# #     # CASE 2
# #     # Direct text field
# #     # ------------------------------------------------------

# #     text = payload.get(
# #         "text"
# #     )

# #     if text:

# #         return str(text).strip()


# #     # ------------------------------------------------------
# #     # CASE 3
# #     # Direct content field
# #     # ------------------------------------------------------

# #     content = payload.get(
# #         "content"
# #     )

# #     if content:

# #         return str(content).strip()


# #     return ""


# # # ==========================================================
# # # RETRIEVE DOCUMENT CHUNKS
# # # ==========================================================

# # def retrieve(
# #     query: str,
# #     top_k: int = TOP_K,
# # ):

# #     print("\n" + "=" * 60)
# #     print("USER QUERY")
# #     print("=" * 60)

# #     print(query)


# #     # ------------------------------------------------------
# #     # EMBED USER QUERY
# #     # ------------------------------------------------------

# #     query_embedding = embed_model.get_text_embedding(
# #         query
# #     )


# #     print(
# #         f"\nQuery embedding dimension: "
# #         f"{len(query_embedding)}"
# #     )


# #     # ------------------------------------------------------
# #     # SEARCH QDRANT
# #     # ------------------------------------------------------

# #     results = qdrant_client.query_points(

# #         collection_name=COLLECTION_NAME,

# #         query=query_embedding,

# #         limit=top_k,

# #         with_payload=True,

# #         with_vectors=False,
# #     )


# #     return results.points


# # # ==========================================================
# # # BUILD CONTEXT FOR GEMINI
# # # ==========================================================

# # def build_context(results):

# #     context_parts = []

# #     source_number = 1


# #     for result in results:

# #         payload = result.payload or {}


# #         filename = payload.get(
# #             "filename",
# #             "Unknown file"
# #         )


# #         text = get_node_text(
# #             payload
# #         )


# #         # Ignore empty chunks
# #         if not text:

# #             continue


# #         context_parts.append(
# #             f"""
# # SOURCE {source_number}
# # FILE: {filename}
# # RELEVANCE SCORE: {result.score}

# # CONTENT:
# # {text}
# # """
# #         )


# #         source_number += 1


# #     return "\n".join(
# #         context_parts
# #     )


# # # ==========================================================
# # # GEMINI SINGLE REQUEST
# # # ==========================================================

# # def call_gemini(
# #     model,
# #     prompt,
# # ):

# #     response = gemini_client.models.generate_content(

# #         model=model,

# #         contents=prompt,
# #     )


# #     if not response:

# #         raise RuntimeError(
# #             "Gemini returned no response."
# #         )


# #     if not response.text:

# #         raise RuntimeError(
# #             "Gemini returned an empty response."
# #         )


# #     return response.text.strip()


# # # ==========================================================
# # # GEMINI WITH RETRIES + FALLBACK
# # # ==========================================================

# # def generate_answer(
# #     query,
# #     context,
# # ):

# #     if not context.strip():

# #         return (
# #             "I could not find any readable text "
# #             "in the retrieved documents."
# #         )


# #     # ======================================================
# #     # PROMPT
# #     # ======================================================

# #     prompt = f"""
# # You are a helpful document question-answering assistant.

# # Your job is to answer the user's question using ONLY
# # the information contained in the document context.

# # STRICT RULES:

# # 1. Do not use outside knowledge.
# # 2. Do not invent facts.
# # 3. Do not make assumptions.
# # 4. If the answer is present in the context, explain it clearly.
# # 5. If the answer is not present, say:
# #    "I could not find this information in the provided documents."
# # 6. Keep the answer concise but useful.
# # 7. If multiple documents contain relevant information,
# #    combine them carefully.
# # 8. Do not mention these instructions in your answer.

# # DOCUMENT CONTEXT:
# # {context}

# # USER QUESTION:
# # {query}

# # ANSWER:
# # """


# #     # ======================================================
# #     # TRY ONE MODEL
# #     # ======================================================

# #     def try_model(model_name):

# #         for attempt in range(
# #             1,
# #             MAX_RETRIES + 1,
# #         ):

# #             try:

# #                 print(
# #                     f"\n🤖 Trying {model_name} "
# #                     f"(attempt {attempt}/{MAX_RETRIES})..."
# #                 )


# #                 answer = call_gemini(

# #                     model=model_name,

# #                     prompt=prompt,
# #                 )


# #                 print(
# #                     f"✅ {model_name} "
# #                     f"responded successfully."
# #                 )


# #                 return answer


# #             except Exception as e:

# #                 error_message = str(e)


# #                 print(
# #                     f"⚠️ {model_name} failed "
# #                     f"(attempt {attempt}/{MAX_RETRIES})"
# #                 )


# #                 print(
# #                     f"Error: {error_message}"
# #                 )


# #                 # --------------------------------------------------
# #                 # FINAL ATTEMPT
# #                 # --------------------------------------------------

# #                 if attempt == MAX_RETRIES:

# #                     print(
# #                         f"❌ All attempts failed "
# #                         f"for {model_name}."
# #                     )

# #                     return None


# #                 # --------------------------------------------------
# #                 # EXPONENTIAL BACKOFF
# #                 # --------------------------------------------------

# #                 delay = INITIAL_RETRY_DELAY * (
# #                     2 ** (attempt - 1)
# #                 )


# #                 print(
# #                     f"⏳ Waiting {delay} seconds "
# #                     f"before retry..."
# #                 )


# #                 time.sleep(
# #                     delay
# #                 )


# #         return None


# #     # ======================================================
# #     # PRIMARY MODEL
# #     # ======================================================

# #     answer = try_model(
# #         GEMINI_MODEL
# #     )


# #     if answer:

# #         return answer


# #     # ======================================================
# #     # FALLBACK MODEL
# #     # ======================================================

# #     print("\n" + "=" * 60)
# #     print("PRIMARY MODEL FAILED")
# #     print("=" * 60)


# #     print(
# #         f"Trying fallback model: "
# #         f"{FALLBACK_MODEL}"
# #     )


# #     answer = try_model(
# #         FALLBACK_MODEL
# #     )


# #     if answer:

# #         return answer


# #     # ======================================================
# #     # BOTH MODELS FAILED
# #     # ======================================================

# #     return (
# #         "I retrieved the relevant information from "
# #         "your documents, but the Gemini service is "
# #         "currently unavailable. Please try the "
# #         "question again in a moment."
# #     )


# # # ==========================================================
# # # MAIN RAG PIPELINE
# # # ==========================================================

# # if __name__ == "__main__":

# #     try:

# #         # ==================================================
# #         # USER QUERY
# #         # ==================================================

# #         query = input(
# #             "\nAsk a question about your documents: "
# #         ).strip()


# #         if not query:

# #             print(
# #                 "❌ Please enter a question."
# #             )

# #             raise SystemExit(1)


# #         # ==================================================
# #         # STEP 0 — REDIS CACHE CHECK
# #         # ==================================================

# #         print("\n" + "=" * 60)
# #         print("CHECKING REDIS CACHE")
# #         print("=" * 60)


# #         redis_available = is_redis_alive()


# #         if redis_available:

# #             print(
# #                 "✅ Redis is connected"
# #             )


# #             cached_answer = get_cached_answer(
# #                 query
# #             )


# #             # ------------------------------------------------
# #             # CACHE HIT
# #             # ------------------------------------------------

# #             if cached_answer:

# #                 print(
# #                     "✅ CACHE HIT"
# #                 )


# #                 print(
# #                     "Returning cached answer..."
# #                 )


# #                 print("\n" + "=" * 60)
# #                 print(
# #                     "FINAL ANSWER "
# #                     "(FROM REDIS CACHE)"
# #                 )
# #                 print("=" * 60)


# #                 print(
# #                     cached_answer
# #                 )


# #                 print("\n" + "=" * 60)
# #                 print(
# #                     "RAG PIPELINE COMPLETED"
# #                 )
# #                 print("=" * 60)


# #                 raise SystemExit(0)


# #             # ------------------------------------------------
# #             # CACHE MISS
# #             # ------------------------------------------------

# #             print(
# #                 "❌ CACHE MISS"
# #             )


# #             print(
# #                 "Question not found in Redis."
# #             )


# #         else:

# #             print(
# #                 "⚠️ Redis is unavailable."
# #             )


# #             print(
# #                 "Continuing without cache..."
# #             )


# #         # ==================================================
# #         # STEP 1 — QDRANT RETRIEVAL
# #         # ==================================================

# #         results = retrieve(
# #             query
# #         )


# #         print("\n" + "=" * 60)
# #         print("RETRIEVED CHUNKS")
# #         print("=" * 60)


# #         if not results:

# #             print(
# #                 "❌ No results found."
# #             )

# #             raise SystemExit(0)


# #         # ==================================================
# #         # STEP 2 — DISPLAY RETRIEVED CHUNKS
# #         # ==================================================

# #         for i, result in enumerate(
# #             results,
# #             start=1,
# #         ):

# #             print("\n" + "-" * 60)
# #             print(
# #                 f"RESULT {i}"
# #             )
# #             print("-" * 60)


# #             print(
# #                 f"Score: {result.score}"
# #             )


# #             payload = (
# #                 result.payload or {}
# #             )


# #             print(
# #                 f"File: "
# #                 f"{payload.get('filename', 'Unknown')}"
# #             )


# #             print(
# #                 f"Extension: "
# #                 f"{payload.get('extension', 'Unknown')}"
# #             )


# #             text = get_node_text(
# #                 payload
# #             )


# #             print("\nText:")


# #             if text:

# #                 print(text)

# #             else:

# #                 print(
# #                     "⚠️ No text found."
# #                 )


# #         # ==================================================
# #         # STEP 3 — BUILD CONTEXT
# #         # ==================================================

# #         context = build_context(
# #             results
# #         )


# #         if not context.strip():

# #             print(
# #                 "\n❌ Retrieved chunks "
# #                 "contain no readable text."
# #             )


# #             raise SystemExit(0)


# #         # ==================================================
# #         # STEP 4 — GENERATE ANSWER
# #         # ==================================================

# #         print("\n" + "=" * 60)
# #         print("GENERATING ANSWER")
# #         print("=" * 60)


# #         answer = generate_answer(

# #             query=query,

# #             context=context,
# #         )


# #         # ==================================================
# #         # STEP 5 — SAVE ANSWER TO REDIS
# #         # ==================================================

# #         if redis_available:

# #             print("\n" + "=" * 60)
# #             print("SAVING ANSWER TO REDIS")
# #             print("=" * 60)


# #             cache_answer(

# #                 question=query,

# #                 answer=answer,
# #             )


# #             print(
# #                 "✅ Answer cached successfully"
# #             )


# #             print(
# #                 "⏱️ Cache expiration: 1 hour"
# #             )


# #         else:

# #             print(
# #                 "⚠️ Redis unavailable."
# #             )


# #             print(
# #                 "Answer will not be cached."
# #             )


# #         # ==================================================
# #         # STEP 6 — FINAL ANSWER
# #         # ==================================================

# #         print("\n" + "=" * 60)
# #         print("FINAL ANSWER")
# #         print("=" * 60)


# #         print(
# #             answer
# #         )


# #         print("\n" + "=" * 60)
# #         print("RAG PIPELINE COMPLETED")
# #         print("=" * 60)


# #     finally:

# #         qdrant_client.close()



# import os
# import json
# import time

# from dotenv import load_dotenv
# from google import genai
# from qdrant_client import QdrantClient

# from embedding import embed_model

# from redis_cache import (
#     get_cached_answer,
#     cache_answer,
#     is_redis_alive,
#     normalize_query,
# )


# # ==========================================================
# # CONFIGURATION
# # ==========================================================

# QDRANT_PATH = "./qdrant_db"
# COLLECTION_NAME = "documents"

# TOP_K = 3


# # ==========================================================
# # GEMINI CONFIGURATION
# # ==========================================================

# GEMINI_MODEL = "gemini-3.6-flash"
# FALLBACK_MODEL = "gemini-3.5-flash"

# MAX_RETRIES = 3
# INITIAL_RETRY_DELAY = 2


# # ==========================================================
# # CHAT CONFIGURATION
# # ==========================================================

# EXIT_COMMANDS = {
#     "bye",
#     "goodbye",
#     "exit",
#     "quit",
#     "q",
# }

# # Number of complete conversation exchanges
# MAX_HISTORY_TURNS = 10

# # This means:
# # 10 user messages + 10 assistant messages
# MAX_HISTORY_MESSAGES = MAX_HISTORY_TURNS * 2


# # ==========================================================
# # CONFIGURE GEMINI
# # ==========================================================

# load_dotenv()

# api_key = os.getenv("GOOGLE_API_KEY")

# if not api_key:
#     raise RuntimeError(
#         "GOOGLE_API_KEY not found in environment variables."
#     )

# gemini_client = genai.Client(
#     api_key=api_key
# )


# # ==========================================================
# # CONNECT TO QDRANT
# # ==========================================================

# print("Connecting to Qdrant...")

# qdrant_client = QdrantClient(
#     path=QDRANT_PATH
# )

# print("✅ Qdrant connected")


# # ==========================================================
# # CHECK COLLECTION
# # ==========================================================

# collections = qdrant_client.get_collections()

# collection_names = [
#     collection.name
#     for collection in collections.collections
# ]

# if COLLECTION_NAME not in collection_names:

#     qdrant_client.close()

#     raise RuntimeError(
#         f"Collection '{COLLECTION_NAME}' does not exist."
#     )

# print(
#     f"✅ Collection '{COLLECTION_NAME}' found"
# )


# # ==========================================================
# # EXTRACT TEXT FROM QDRANT PAYLOAD
# # ==========================================================

# def get_node_text(payload):
#     """
#     Extract original chunk text from a LlamaIndex payload.
#     """

#     if not payload:
#         return ""


#     # ------------------------------------------------------
#     # CASE 1
#     # LlamaIndex TextNode stored as JSON
#     # ------------------------------------------------------

#     node_content = payload.get(
#         "_node_content"
#     )

#     if node_content:

#         try:

#             node_data = json.loads(
#                 node_content
#             )

#             text = node_data.get(
#                 "text"
#             )

#             if text:
#                 return text.strip()

#         except (
#             json.JSONDecodeError,
#             TypeError,
#         ):

#             pass


#     # ------------------------------------------------------
#     # CASE 2
#     # Direct text field
#     # ------------------------------------------------------

#     text = payload.get(
#         "text"
#     )

#     if text:
#         return str(text).strip()


#     # ------------------------------------------------------
#     # CASE 3
#     # Direct content field
#     # ------------------------------------------------------

#     content = payload.get(
#         "content"
#     )

#     if content:
#         return str(content).strip()


#     return ""


# # ==========================================================
# # RETRIEVE DOCUMENT CHUNKS
# # ==========================================================

# def retrieve(
#     query: str,
#     top_k: int = TOP_K,
# ):

#     print("\n" + "=" * 60)
#     print("QDRANT RETRIEVAL")
#     print("=" * 60)

#     print(
#         f"Retrieval query: {query}"
#     )


#     # ------------------------------------------------------
#     # EMBED QUERY
#     # ------------------------------------------------------

#     query_embedding = (
#         embed_model.get_text_embedding(
#             query
#         )
#     )


#     print(
#         f"Query embedding dimension: "
#         f"{len(query_embedding)}"
#     )


#     # ------------------------------------------------------
#     # SEARCH QDRANT
#     # ------------------------------------------------------

#     results = qdrant_client.query_points(

#         collection_name=COLLECTION_NAME,

#         query=query_embedding,

#         limit=top_k,

#         with_payload=True,

#         with_vectors=False,

#     )


#     return results.points


# # ==========================================================
# # BUILD DOCUMENT CONTEXT
# # ==========================================================

# def build_context(results):

#     context_parts = []

#     source_number = 1


#     for result in results:

#         payload = result.payload or {}


#         filename = payload.get(
#             "filename",
#             "Unknown file"
#         )


#         text = get_node_text(
#             payload
#         )


#         if not text:
#             continue


#         context_parts.append(

#             f"""
# SOURCE {source_number}

# FILE:
# {filename}

# RELEVANCE SCORE:
# {result.score}

# CONTENT:
# {text}
# """
#         )


#         source_number += 1


#     return "\n".join(
#         context_parts
#     )


# # ==========================================================
# # BUILD CONVERSATION HISTORY
# # ==========================================================

# def build_history_context(
#     conversation_history
# ):

#     if not conversation_history:

#         return "No previous conversation."


#     # ------------------------------------------------------
#     # Keep latest N complete conversation turns
#     # ------------------------------------------------------

#     recent_history = conversation_history[
#         -MAX_HISTORY_MESSAGES:
#     ]


#     history_parts = []


#     for message in recent_history:

#         role = message["role"]

#         content = message["content"]


#         if role == "user":

#             history_parts.append(
#                 f"USER: {content}"
#             )


#         elif role == "assistant":

#             history_parts.append(
#                 f"ASSISTANT: {content}"
#             )


#     return "\n".join(
#         history_parts
#     )


# # ==========================================================
# # CHECK CURRENT CONVERSATION MEMORY
# # ==========================================================

# def get_answer_from_conversation_memory(
#     query,
#     conversation_history,
# ):

#     normalized_current_query = (
#         normalize_query(query)
#     )


#     # Walk backwards through previous user messages
#     # so the most recent matching question wins.

#     for i in range(
#         len(conversation_history) - 1,
#         -1,
#         -1,
#     ):

#         message = conversation_history[i]


#         if message["role"] != "user":
#             continue


#         previous_question = message["content"]


#         normalized_previous_question = (
#             normalize_query(
#                 previous_question
#             )
#         )


#         if (
#             normalized_previous_question
#             != normalized_current_query
#         ):

#             continue


#         # --------------------------------------------------
#         # Find assistant response immediately after
#         # this user question.
#         # --------------------------------------------------

#         if i + 1 < len(conversation_history):

#             next_message = (
#                 conversation_history[i + 1]
#             )


#             if (
#                 next_message["role"]
#                 == "assistant"
#             ):

#                 return next_message["content"]


#     return None


# # ==========================================================
# # BUILD RETRIEVAL QUERY
# # ==========================================================

# def build_retrieval_query(
#     current_query,
#     conversation_history,
# ):

#     if not conversation_history:

#         return current_query


#     # ------------------------------------------------------
#     # Use recent conversation for retrieval.
#     #
#     # This helps follow-up questions like:
#     #
#     # "Who is Devanshi?"
#     # "What does she study?"
#     # "Where does she study?"
#     # ------------------------------------------------------

#     recent_history = conversation_history[
#         -6:
#     ]


#     history_questions = []


#     for message in recent_history:

#         if message["role"] == "user":

#             history_questions.append(
#                 message["content"]
#             )


#     if not history_questions:

#         return current_query


#     retrieval_query = (

#         "Previous conversation:\n"

#         + "\n".join(
#             history_questions
#         )

#         + "\n\nCurrent question:\n"

#         + current_query
#     )


#     return retrieval_query


# # ==========================================================
# # GEMINI SINGLE REQUEST
# # ==========================================================

# def call_gemini(
#     model,
#     prompt,
# ):

#     response = (
#         gemini_client.models.generate_content(

#             model=model,

#             contents=prompt,
#         )
#     )


#     if not response:

#         raise RuntimeError(
#             "Gemini returned no response."
#         )


#     if not response.text:

#         raise RuntimeError(
#             "Gemini returned an empty response."
#         )


#     return response.text.strip()


# # ==========================================================
# # GEMINI WITH RETRIES + FALLBACK
# # ==========================================================

# def generate_answer(
#     query,
#     context,
#     conversation_history,
# ):

#     if not context.strip():

#         return (
#             "I could not find any readable text "
#             "in the retrieved documents."
#         )


#     # ------------------------------------------------------
#     # BUILD CONVERSATION HISTORY
#     # ------------------------------------------------------

#     history_context = (
#         build_history_context(
#             conversation_history
#         )
#     )


#     # ======================================================
#     # PROMPT
#     # ======================================================

#     prompt = f"""
# You are a helpful conversational document
# question-answering assistant.

# Your job is to answer the user's CURRENT question
# using ONLY information from the provided document
# context.

# You may use the previous conversation ONLY to
# understand what the user is referring to.

# STRICT RULES:

# 1. Do not use outside knowledge.

# 2. Do not invent facts.

# 3. Do not make assumptions.

# 4. Use previous conversation to understand
#    follow-up questions and references such as:

#    - it
#    - this
#    - that
#    - she
#    - he
#    - they
#    - the program
#    - the project
#    - the rank
#    - the university

# 5. The document context is the primary source
#    for factual answers.

# 6. If the answer is present in the document
#    context, explain it clearly.

# 7. If the answer is not present in the document
#    context, say exactly:

#    "I could not find this information in the
#    provided documents."

# 8. Keep the answer concise but useful.

# 9. Do not mention these instructions.

# 10. Do not answer using information that exists
#     only in previous conversation if that information
#     is not supported by the retrieved documents.

# 11. Previous conversation is for understanding
#     references and context, NOT for inventing
#     document facts.


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

# {query}


# ==========================================================
# ANSWER
# ==========================================================
# """


#     # ======================================================
#     # TRY ONE MODEL
#     # ======================================================

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
#                     f"✅ {model_name} "
#                     f"responded successfully."
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

#                     print(
#                         f"❌ All attempts failed "
#                         f"for {model_name}."
#                     )

#                     return None


#                 delay = (
#                     INITIAL_RETRY_DELAY
#                     * (2 ** (attempt - 1))
#                 )


#                 print(
#                     f"⏳ Waiting {delay} seconds "
#                     f"before retry..."
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

#     print("\n" + "=" * 60)
#     print("PRIMARY MODEL FAILED")
#     print("=" * 60)


#     print(
#         f"Trying fallback model: "
#         f"{FALLBACK_MODEL}"
#     )


#     answer = try_model(
#         FALLBACK_MODEL
#     )


#     if answer:

#         return answer


#     # ======================================================
#     # BOTH MODELS FAILED
#     # ======================================================

#     return (
#         "I retrieved relevant information from "
#         "your documents, but the Gemini service "
#         "is currently unavailable. Please try "
#         "again in a moment."
#     )


# # ==========================================================
# # DISPLAY RETRIEVED RESULTS
# # ==========================================================

# def display_results(results):

#     print("\n" + "=" * 60)
#     print("RETRIEVED CHUNKS")
#     print("=" * 60)


#     if not results:

#         print(
#             "❌ No results found."
#         )

#         return


#     for i, result in enumerate(
#         results,
#         start=1,
#     ):

#         print("\n" + "-" * 60)

#         print(
#             f"RESULT {i}"
#         )

#         print("-" * 60)


#         print(
#             f"Score: {result.score}"
#         )


#         payload = (
#             result.payload or {}
#         )


#         print(
#             f"File: "
#             f"{payload.get('filename', 'Unknown')}"
#         )


#         print(
#             f"Extension: "
#             f"{payload.get('extension', 'Unknown')}"
#         )


#         text = get_node_text(
#             payload
#         )


#         print("\nText:")


#         if text:

#             print(text)

#         else:

#             print(
#                 "⚠️ No text found."
#             )


# # ==========================================================
# # MAIN CONVERSATIONAL RAG CHATBOT
# # ==========================================================

# if __name__ == "__main__":

#     try:

#         # ==================================================
#         # CONVERSATION MEMORY
#         # ==================================================

#         conversation_history = []


#         # ==================================================
#         # REDIS STATUS
#         # ==================================================

#         redis_available = is_redis_alive()


#         print("\n" + "=" * 60)
#         print("REDIS STATUS")
#         print("=" * 60)


#         if redis_available:

#             print(
#                 "✅ Redis is connected"
#             )

#         else:

#             print(
#                 "⚠️ Redis is unavailable."
#             )

#             print(
#                 "Continuing without answer cache."
#             )


#         # ==================================================
#         # START CHAT
#         # ==================================================

#         print("\n" + "=" * 60)
#         print("🤖 RAG CHATBOT READY")
#         print("=" * 60)


#         print(
#             "Ask questions about your documents."
#         )


#         print(
#             "I will remember the current conversation."
#         )


#         print(
#             "Type 'bye' or 'goodbye' to exit."
#         )


#         # ==================================================
#         # CONTINUOUS CHAT LOOP
#         # ==================================================

#         while True:

#             print()


#             query = input(
#                 "You: "
#             ).strip()


#             # ------------------------------------------------
#             # EMPTY INPUT
#             # ------------------------------------------------

#             if not query:

#                 print(
#                     "Please enter a question."
#                 )

#                 continue


#             # ------------------------------------------------
#             # EXIT CHECK
#             # ------------------------------------------------

#             normalized_exit_query = (
#                 normalize_query(query)
#             )


#             if (
#                 normalized_exit_query
#                 in EXIT_COMMANDS
#             ):

#                 print(
#                     "\n🤖 Goodbye! 👋"
#                 )

#                 break


#             # =================================================
#             # STEP 0
#             # CHECK CURRENT CONVERSATION MEMORY
#             # =================================================

#             print("\n" + "=" * 60)
#             print("CHECKING CONVERSATION MEMORY")
#             print("=" * 60)


#             conversation_cached_answer = (
#                 get_answer_from_conversation_memory(

#                     query=query,

#                     conversation_history=(
#                         conversation_history
#                     ),

#                 )
#             )


#             if conversation_cached_answer:

#                 print(
#                     "🟢 CONVERSATION MEMORY HIT"
#                 )


#                 print(
#                     "Gemini will NOT be called."
#                 )


#                 answer = (
#                     conversation_cached_answer
#                 )


#                 print("\n" + "=" * 60)
#                 print("🤖 ASSISTANT")
#                 print("=" * 60)


#                 print(
#                     answer
#                 )


#                 # ------------------------------------------------
#                 # We do NOT append this same question/answer
#                 # again because it is already stored.
#                 # ------------------------------------------------

#                 continue


#             print(
#                 "❌ Conversation memory miss"
#             )


#             # =================================================
#             # STEP 1
#             # CHECK REDIS CACHE
#             # =================================================

#             cached_answer = None


#             if redis_available:

#                 print("\n" + "=" * 60)
#                 print("CHECKING REDIS CACHE")
#                 print("=" * 60)


#                 cached_answer = (
#                     get_cached_answer(
#                         query
#                     )
#                 )


#                 if cached_answer:

#                     print(
#                         "🟢 REDIS CACHE HIT"
#                     )


#                     print(
#                         "Gemini will NOT be called."
#                     )


#                     answer = cached_answer


#                     # --------------------------------------------
#                     # IMPORTANT:
#                     #
#                     # Add Redis answer to conversation memory.
#                     #
#                     # This allows the next question to understand
#                     # the cached answer as part of the conversation.
#                     # --------------------------------------------

#                     conversation_history.append({

#                         "role": "user",

#                         "content": query,

#                     })


#                     conversation_history.append({

#                         "role": "assistant",

#                         "content": answer,

#                     })


#                     print("\n" + "=" * 60)
#                     print("🤖 ASSISTANT")
#                     print("=" * 60)


#                     print(
#                         answer
#                     )


#                     continue


#                 else:

#                     print(
#                         "🔴 REDIS CACHE MISS"
#                     )


#             else:

#                 print(
#                     "⚠️ Redis unavailable."
#                 )


#             # =================================================
#             # STEP 2
#             # BUILD CONTEXT-AWARE RETRIEVAL QUERY
#             # =================================================

#             retrieval_query = (
#                 build_retrieval_query(

#                     current_query=query,

#                     conversation_history=(
#                         conversation_history
#                     ),

#                 )
#             )


#             # =================================================
#             # STEP 3
#             # QDRANT RETRIEVAL
#             # =================================================

#             results = retrieve(
#                 retrieval_query
#             )


#             display_results(
#                 results
#             )


#             if not results:

#                 answer = (
#                     "I could not find relevant "
#                     "information in the documents."
#                 )


#                 print("\n" + "=" * 60)
#                 print("🤖 ASSISTANT")
#                 print("=" * 60)


#                 print(
#                     answer
#                 )


#                 # --------------------------------------------
#                 # Save conversation
#                 # --------------------------------------------

#                 conversation_history.append({

#                     "role": "user",

#                     "content": query,

#                 })


#                 conversation_history.append({

#                     "role": "assistant",

#                     "content": answer,

#                 })


#                 continue


#             # =================================================
#             # STEP 4
#             # BUILD DOCUMENT CONTEXT
#             # =================================================

#             context = build_context(
#                 results
#             )


#             if not context.strip():

#                 answer = (
#                     "I could not find any readable "
#                     "text in the retrieved documents."
#                 )


#                 print("\n" + "=" * 60)
#                 print("🤖 ASSISTANT")
#                 print("=" * 60)


#                 print(
#                     answer
#                 )


#                 conversation_history.append({

#                     "role": "user",

#                     "content": query,

#                 })


#                 conversation_history.append({

#                     "role": "assistant",

#                     "content": answer,

#                 })


#                 continue


#             # =================================================
#             # STEP 5
#             # CALL GEMINI
#             # =================================================

#             print("\n" + "=" * 60)
#             print("GENERATING ANSWER")
#             print("=" * 60)


#             answer = generate_answer(

#                 query=query,

#                 context=context,

#                 conversation_history=(
#                     conversation_history
#                 ),

#             )


#             # =================================================
#             # STEP 6
#             # SAVE ANSWER TO REDIS
#             # =================================================

#             if redis_available:

#                 print("\n" + "=" * 60)
#                 print("SAVING ANSWER TO REDIS")
#                 print("=" * 60)


#                 cache_answer(

#                     question=query,

#                     answer=answer,

#                 )


#                 print(
#                     "✅ Answer cached successfully."
#                 )


#                 print(
#                     "⏱️ Cache expiration: 1 hour."
#                 )


#             # =================================================
#             # STEP 7
#             # SAVE TO CONVERSATION MEMORY
#             # =================================================

#             conversation_history.append({

#                 "role": "user",

#                 "content": query,

#             })


#             conversation_history.append({

#                 "role": "assistant",

#                 "content": answer,

#             })


#             # =================================================
#             # STEP 8
#             # SHOW FINAL ANSWER
#             # =================================================

#             print("\n" + "=" * 60)
#             print("🤖 ASSISTANT")
#             print("=" * 60)


#             print(
#                 answer
#             )


#             print("\n" + "=" * 60)

#             print(
#                 f"Conversation memory: "
#                 f"{len(conversation_history) // 2} turn(s)"
#             )

#             print("=" * 60)


#     except KeyboardInterrupt:

#         print(
#             "\n\n🤖 Chat stopped."
#         )


#     finally:

#         qdrant_client.close()

#         print(
#             "Qdrant connection closed."
#         )







import os
import json
import time

from dotenv import load_dotenv
from google import genai
from qdrant_client import QdrantClient

from embedding import embed_model

from redis_cache import (
    get_cached_answer,
    cache_answer,
    is_redis_alive,
    normalize_query,
)


# ==========================================================
# CONFIGURATION
# ==========================================================

# QDRANT_PATH = "./qdrant_db"
# COLLECTION_NAME = "documents"
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = "documents"

TOP_K = 3


# ==========================================================
# GEMINI CONFIGURATION
# ==========================================================

GEMINI_MODEL = "gemini-3.6-flash"
FALLBACK_MODEL = "gemini-3.5-flash"

MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 2


# ==========================================================
# CHAT CONFIGURATION
# ==========================================================

EXIT_COMMANDS = {
    "bye",
    "goodbye",
    "exit",
    "quit",
    "q",
}

# Maximum number of complete conversation turns
MAX_HISTORY_TURNS = 10

# 1 turn = 1 user message + 1 assistant message
MAX_HISTORY_MESSAGES = MAX_HISTORY_TURNS * 2


# ==========================================================
# CONFIGURE GEMINI
# ==========================================================

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise RuntimeError(
        "GOOGLE_API_KEY not found in environment variables."
    )

gemini_client = genai.Client(
    api_key=api_key
)


# ==========================================================
# CONNECT TO QDRANT
# ==========================================================

print("Connecting to Qdrant...")

# qdrant_client = QdrantClient(
#     path=QDRANT_PATH
# )
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

print("✅ Qdrant connected")


# ==========================================================
# CHECK COLLECTION
# ==========================================================

collections = qdrant_client.get_collections()

collection_names = [
    collection.name
    for collection in collections.collections
]

if COLLECTION_NAME not in collection_names:

    qdrant_client.close()

    raise RuntimeError(
        f"Collection '{COLLECTION_NAME}' does not exist."
    )

print(
    f"✅ Collection '{COLLECTION_NAME}' found"
)


# ==========================================================
# EXTRACT TEXT FROM QDRANT PAYLOAD
# ==========================================================

def get_node_text(payload):
    """
    Extract original chunk text from a LlamaIndex payload.
    """

    if not payload:
        return ""


    # ------------------------------------------------------
    # CASE 1
    # LlamaIndex TextNode stored as JSON
    # ------------------------------------------------------

    node_content = payload.get(
        "_node_content"
    )

    if node_content:

        try:

            node_data = json.loads(
                node_content
            )

            text = node_data.get(
                "text"
            )

            if text:
                return text.strip()

        except (
            json.JSONDecodeError,
            TypeError,
        ):

            pass


    # ------------------------------------------------------
    # CASE 2
    # Direct text field
    # ------------------------------------------------------

    text = payload.get(
        "text"
    )

    if text:
        return str(text).strip()


    # ------------------------------------------------------
    # CASE 3
    # Direct content field
    # ------------------------------------------------------

    content = payload.get(
        "content"
    )

    if content:
        return str(content).strip()


    return ""


# ==========================================================
# RETRIEVE DOCUMENT CHUNKS
# ==========================================================

def retrieve(
    query: str,
    top_k: int = TOP_K,
):

    print("\n" + "=" * 60)
    print("QDRANT RETRIEVAL")
    print("=" * 60)

    print(
        f"Retrieval query: {query}"
    )


    # ------------------------------------------------------
    # EMBED QUERY
    # ------------------------------------------------------

    query_embedding = (
        embed_model.get_text_embedding(
            query
        )
    )


    print(
        f"Query embedding dimension: "
        f"{len(query_embedding)}"
    )


    # ------------------------------------------------------
    # SEARCH QDRANT
    # ------------------------------------------------------

    results = qdrant_client.query_points(

        collection_name=COLLECTION_NAME,

        query=query_embedding,

        limit=top_k,

        with_payload=True,

        with_vectors=False,

    )


    return results.points


# ==========================================================
# BUILD DOCUMENT CONTEXT
# ==========================================================

def build_context(results):

    context_parts = []

    source_number = 1


    for result in results:

        payload = result.payload or {}


        filename = payload.get(
            "filename",
            "Unknown file"
        )


        text = get_node_text(
            payload
        )


        if not text:
            continue


        context_parts.append(

            f"""
SOURCE {source_number}

FILE:
{filename}

RELEVANCE SCORE:
{result.score}

CONTENT:
{text}
"""
        )


        source_number += 1


    return "\n".join(
        context_parts
    )


# ==========================================================
# BUILD CONVERSATION HISTORY
# ==========================================================

def build_history_context(
    conversation_history
):

    if not conversation_history:

        return "No previous conversation."


    # ------------------------------------------------------
    # Keep latest N complete conversation turns
    # ------------------------------------------------------

    recent_history = conversation_history[
        -MAX_HISTORY_MESSAGES:
    ]


    history_parts = []


    for message in recent_history:

        role = message["role"]

        content = message["content"]


        if role == "user":

            history_parts.append(
                f"USER: {content}"
            )


        elif role == "assistant":

            history_parts.append(
                f"ASSISTANT: {content}"
            )


    return "\n".join(
        history_parts
    )


# ==========================================================
# CHECK CURRENT CONVERSATION MEMORY
# ==========================================================

def get_answer_from_conversation_memory(
    query,
    conversation_history,
):

    normalized_current_query = (
        normalize_query(query)
    )


    # ------------------------------------------------------
    # Walk backwards through previous user messages
    # ------------------------------------------------------

    for i in range(
        len(conversation_history) - 1,
        -1,
        -1,
    ):

        message = conversation_history[i]


        if message["role"] != "user":
            continue


        previous_question = message["content"]


        normalized_previous_question = (
            normalize_query(
                previous_question
            )
        )


        if (
            normalized_previous_question
            != normalized_current_query
        ):

            continue


        # --------------------------------------------------
        # Find assistant response immediately after
        # this user question.
        # --------------------------------------------------

        if i + 1 < len(conversation_history):

            next_message = (
                conversation_history[i + 1]
            )


            if (
                next_message["role"]
                == "assistant"
            ):

                return next_message["content"]


    return None


# ==========================================================
# BUILD RETRIEVAL QUERY
# ==========================================================

def build_retrieval_query(
    current_query,
    conversation_history,
):

    if not conversation_history:

        return current_query


    # ------------------------------------------------------
    # Use recent conversation for retrieval.
    # ------------------------------------------------------

    recent_history = conversation_history[
        -6:
    ]


    history_questions = []


    for message in recent_history:

        if message["role"] == "user":

            history_questions.append(
                message["content"]
            )


    if not history_questions:

        return current_query


    retrieval_query = (

        "Previous conversation:\n"

        + "\n".join(
            history_questions
        )

        + "\n\nCurrent question:\n"

        + current_query
    )


    return retrieval_query


# ==========================================================
# GEMINI SINGLE REQUEST
# ==========================================================

def call_gemini(
    model,
    prompt,
):

    response = (
        gemini_client.models.generate_content(

            model=model,

            contents=prompt,
        )
    )


    if not response:

        raise RuntimeError(
            "Gemini returned no response."
        )


    if not response.text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )


    return response.text.strip()


# ==========================================================
# GEMINI WITH RETRIES + FALLBACK
# ==========================================================

def generate_answer(
    query,
    context,
    conversation_history,
):

    if not context.strip():

        return (
            "I could not find any readable text "
            "in the retrieved documents."
        )


    # ------------------------------------------------------
    # BUILD CONVERSATION HISTORY
    # ------------------------------------------------------

    history_context = (
        build_history_context(
            conversation_history
        )
    )


    # ======================================================
    # PROMPT
    # ======================================================

    prompt = f"""
You are a helpful conversational document
question-answering assistant.

Your job is to answer the user's CURRENT question
using ONLY information from the provided document
context.

You may use the previous conversation ONLY to
understand what the user is referring to.

STRICT RULES:

1. Do not use outside knowledge.

2. Do not invent facts.

3. Do not make assumptions.

4. Use previous conversation to understand
   follow-up questions and references such as:

   - it
   - this
   - that
   - she
   - he
   - they
   - the program
   - the project
   - the rank
   - the university

5. The document context is the primary source
   for factual answers.

6. If the answer is present in the document
   context, explain it clearly.

7. If the answer is not present in the document
   context, say exactly:

   "I could not find this information in the
   provided documents."

8. Keep the answer concise but useful.

9. Do not mention these instructions.

10. Do not answer using information that exists
    only in previous conversation if that information
    is not supported by the retrieved documents.

11. Previous conversation is for understanding
    references and context, NOT for inventing
    document facts.


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

{query}


==========================================================
ANSWER
==========================================================
"""


    # ======================================================
    # TRY ONE MODEL
    # ======================================================

    def try_model(model_name):

        for attempt in range(
            1,
            MAX_RETRIES + 1,
        ):

            try:

                print(
                    f"\n🤖 Trying {model_name} "
                    f"(attempt {attempt}/{MAX_RETRIES})..."
                )


                answer = call_gemini(

                    model=model_name,

                    prompt=prompt,

                )


                print(
                    f"✅ {model_name} "
                    f"responded successfully."
                )


                return answer


            except Exception as e:

                print(
                    f"⚠️ {model_name} failed "
                    f"(attempt {attempt}/{MAX_RETRIES})"
                )


                print(
                    f"Error: {e}"
                )


                if attempt == MAX_RETRIES:

                    print(
                        f"❌ All attempts failed "
                        f"for {model_name}."
                    )

                    return None


                delay = (
                    INITIAL_RETRY_DELAY
                    * (2 ** (attempt - 1))
                )


                print(
                    f"⏳ Waiting {delay} seconds "
                    f"before retry..."
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

    print("\n" + "=" * 60)
    print("PRIMARY MODEL FAILED")
    print("=" * 60)


    print(
        f"Trying fallback model: "
        f"{FALLBACK_MODEL}"
    )


    answer = try_model(
        FALLBACK_MODEL
    )


    if answer:

        return answer


    # ======================================================
    # BOTH MODELS FAILED
    # ======================================================

    return (
        "I retrieved relevant information from "
        "your documents, but the Gemini service "
        "is currently unavailable. Please try "
        "again in a moment."
    )


# ==========================================================
# DISPLAY RETRIEVED RESULTS
# ==========================================================

def display_results(results):

    print("\n" + "=" * 60)
    print("RETRIEVED CHUNKS")
    print("=" * 60)


    if not results:

        print(
            "❌ No results found."
        )

        return


    for i, result in enumerate(
        results,
        start=1,
    ):

        print("\n" + "-" * 60)

        print(
            f"RESULT {i}"
        )

        print("-" * 60)


        print(
            f"Score: {result.score}"
        )


        payload = (
            result.payload or {}
        )


        print(
            f"File: "
            f"{payload.get('filename', 'Unknown')}"
        )


        print(
            f"Extension: "
            f"{payload.get('extension', 'Unknown')}"
        )


        text = get_node_text(
            payload
        )


        print("\nText:")


        if text:

            print(text)

        else:

            print(
                "⚠️ No text found."
            )


# ==========================================================
# MAIN CONVERSATIONAL RAG CHATBOT
# ==========================================================

if __name__ == "__main__":

    try:

        # ==================================================
        # CONVERSATION MEMORY
        # ==================================================

        conversation_history = []


        # ==================================================
        # REDIS STATUS
        # ==================================================

        redis_available = is_redis_alive()


        print("\n" + "=" * 60)
        print("REDIS STATUS")
        print("=" * 60)


        if redis_available:

            print(
                "✅ Redis is connected"
            )

        else:

            print(
                "⚠️ Redis is unavailable."
            )

            print(
                "Continuing without answer cache."
            )


        # ==================================================
        # START CHAT
        # ==================================================

        print("\n" + "=" * 60)
        print("🤖 RAG CHATBOT READY")
        print("=" * 60)


        print(
            "Ask questions about your documents."
        )


        print(
            "I will remember the current conversation."
        )


        print(
            "Type 'bye', 'goodbye', or 'exit' to exit."
        )


        # ==================================================
        # CONTINUOUS CHAT LOOP
        # ==================================================

        while True:

            print()


            # ------------------------------------------------
            # ALWAYS ASK FOR THE NEXT QUESTION
            # ------------------------------------------------

            query = input(
                "You: "
            ).strip()


            # ------------------------------------------------
            # EMPTY INPUT
            # ------------------------------------------------

            if not query:

                print(
                    "Please enter a question."
                )

                continue


            # ------------------------------------------------
            # EXIT CHECK
            #
            # IMPORTANT:
            # lower() makes this case-insensitive.
            #
            # BYE      -> bye
            # Bye      -> bye
            # GOODBYE  -> goodbye
            # Exit     -> exit
            # ------------------------------------------------

            normalized_exit_query = (
                query.strip().lower()
            )


            if (
                normalized_exit_query
                in EXIT_COMMANDS
            ):

                print(
                    "\n🤖 Goodbye! 👋"
                )

                break


            # =================================================
            # STEP 0
            # CHECK CURRENT CONVERSATION MEMORY
            # =================================================

            print("\n" + "=" * 60)
            print("CHECKING CONVERSATION MEMORY")
            print("=" * 60)


            conversation_cached_answer = (
                get_answer_from_conversation_memory(

                    query=query,

                    conversation_history=(
                        conversation_history
                    ),

                )
            )


            if conversation_cached_answer:

                print(
                    "🟢 CONVERSATION MEMORY HIT"
                )


                print(
                    "Gemini will NOT be called."
                )


                answer = (
                    conversation_cached_answer
                )


                print("\n" + "=" * 60)
                print("🤖 ASSISTANT")
                print("=" * 60)


                print(
                    answer
                )


                # ---------------------------------------------
                # Do not add duplicate question/answer.
                # ---------------------------------------------

                continue


            print(
                "❌ Conversation memory miss"
            )


            # =================================================
            # STEP 1
            # CHECK REDIS CACHE
            # =================================================

            cached_answer = None


            if redis_available:

                print("\n" + "=" * 60)
                print("CHECKING REDIS CACHE")
                print("=" * 60)


                cached_answer = (
                    get_cached_answer(
                        query
                    )
                )


                if cached_answer:

                    print(
                        "🟢 REDIS CACHE HIT"
                    )


                    print(
                        "Gemini will NOT be called."
                    )


                    answer = cached_answer


                    # --------------------------------------------
                    # Add Redis answer to conversation memory.
                    # --------------------------------------------

                    conversation_history.append({

                        "role": "user",

                        "content": query,

                    })


                    conversation_history.append({

                        "role": "assistant",

                        "content": answer,

                    })


                    print("\n" + "=" * 60)
                    print("🤖 ASSISTANT")
                    print("=" * 60)


                    print(
                        answer
                    )


                    # --------------------------------------------
                    # IMPORTANT:
                    #
                    # Continue the while loop and ask for the
                    # next question.
                    # --------------------------------------------

                    continue


                else:

                    print(
                        "🔴 REDIS CACHE MISS"
                    )


            else:

                print(
                    "⚠️ Redis unavailable."
                )


            # =================================================
            # STEP 2
            # BUILD CONTEXT-AWARE RETRIEVAL QUERY
            # =================================================

            retrieval_query = (
                build_retrieval_query(

                    current_query=query,

                    conversation_history=(
                        conversation_history
                    ),

                )
            )


            # =================================================
            # STEP 3
            # QDRANT RETRIEVAL
            # =================================================

            results = retrieve(
                retrieval_query
            )


            display_results(
                results
            )


            if not results:

                answer = (
                    "I could not find relevant "
                    "information in the documents."
                )


                print("\n" + "=" * 60)
                print("🤖 ASSISTANT")
                print("=" * 60)


                print(
                    answer
                )


                # --------------------------------------------
                # Save conversation
                # --------------------------------------------

                conversation_history.append({

                    "role": "user",

                    "content": query,

                })


                conversation_history.append({

                    "role": "assistant",

                    "content": answer,

                })


                # --------------------------------------------
                # Ask next question
                # --------------------------------------------

                continue


            # =================================================
            # STEP 4
            # BUILD DOCUMENT CONTEXT
            # =================================================

            context = build_context(
                results
            )


            if not context.strip():

                answer = (
                    "I could not find any readable "
                    "text in the retrieved documents."
                )


                print("\n" + "=" * 60)
                print("🤖 ASSISTANT")
                print("=" * 60)


                print(
                    answer
                )


                conversation_history.append({

                    "role": "user",

                    "content": query,

                })


                conversation_history.append({

                    "role": "assistant",

                    "content": answer,

                })


                # --------------------------------------------
                # Ask next question
                # --------------------------------------------

                continue


            # =================================================
            # STEP 5
            # CALL GEMINI
            # =================================================

            print("\n" + "=" * 60)
            print("GENERATING ANSWER")
            print("=" * 60)


            answer = generate_answer(

                query=query,

                context=context,

                conversation_history=(
                    conversation_history
                ),

            )


            # =================================================
            # STEP 6
            # SAVE ANSWER TO REDIS
            # =================================================

            if redis_available:

                print("\n" + "=" * 60)
                print("SAVING ANSWER TO REDIS")
                print("=" * 60)


                cache_answer(

                    question=query,

                    answer=answer,

                )


                print(
                    "✅ Answer cached successfully."
                )


                print(
                    "⏱️ Cache expiration: 1 hour."
                )


            # =================================================
            # STEP 7
            # SAVE TO CONVERSATION MEMORY
            # =================================================

            conversation_history.append({

                "role": "user",

                "content": query,

            })


            conversation_history.append({

                "role": "assistant",

                "content": answer,

            })


            # =================================================
            # STEP 8
            # SHOW FINAL ANSWER
            # =================================================

            print("\n" + "=" * 60)
            print("🤖 ASSISTANT")
            print("=" * 60)


            print(
                answer
            )


            print("\n" + "=" * 60)

            print(
                f"Conversation memory: "
                f"{len(conversation_history) // 2} turn(s)"
            )

            print("=" * 60)

            # -----------------------------------------------
            # IMPORTANT:
            #
            # There is NO break here.
            #
            # Because we are inside while True,
            # Python automatically goes back to:
            #
            # query = input("You: ")
            #
            # and waits for the next question.
            # -----------------------------------------------


    except KeyboardInterrupt:

        print(
            "\n\n🤖 Chat stopped."
        )


    finally:

        qdrant_client.close()

        print(
            "Qdrant connection closed."
        )




#---------------------------          new            --------------------------------------



def run_rag_for_evaluation(query):
    """
    Runs one question through the RAG pipeline
    and returns both the generated answer and
    the retrieved contexts.
    """

    # ---------------------------------------------
    # Retrieve chunks
    # ---------------------------------------------

    results = retrieve(query)

    # ---------------------------------------------
    # Extract individual chunk texts
    # ---------------------------------------------

    retrieved_contexts = []

    for result in results:

        payload = result.payload or {}

        text = get_node_text(payload)

        if text:
            retrieved_contexts.append(text)

    # ---------------------------------------------
    # If nothing was retrieved
    # ---------------------------------------------

    if not retrieved_contexts:

        answer = (
            "I could not find relevant information "
            "in the documents."
        )

        return answer, []

    # ---------------------------------------------
    # Build the same context used by your chatbot
    # ---------------------------------------------

    context = build_context(results)

    # ---------------------------------------------
    # Evaluation is single-turn.
    # No previous conversation required.
    # ---------------------------------------------

    answer = generate_answer(
        query=query,
        context=context,
        conversation_history=[],
    )

    return answer, retrieved_contexts