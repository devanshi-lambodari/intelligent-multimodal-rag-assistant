# # # from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
# # # from llama_index.core.node_parser import SentenceSplitter
# # # from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# # # from llama_index.vector_stores.chroma import ChromaVectorStore
# # # from llama_index.core import StorageContext

# # # import chromadb


# # # documents = SimpleDirectoryReader("data").load_data()
# # # print(f"Loaded {len(documents)} documents")

# # # parser = SentenceSplitter(
# # #     chunk_size=254,
# # #     chunk_overlap=40,
# # # )


# # # nodes = parser.get_nodes_from_documents(documents)
# # # print(f"Created {len(nodes)} nodes")


# # # #Load Embedding Model
# # # embed_model = HuggingFaceEmbedding(
# # #     model_name="BAAI/bge-small-en-v1.5"
# # # )


# # # #Create Chroma database
# # # # db = chromadb.PersistentClient(path="./chroma_db")
# # # db = chromadb.PersistentClient(path="./chroma_db")

# # # try:
# # #     db.delete_collection("documents")
# # #     print("Old collection deleted.")
# # # except:
# # #     print("Collection didn't exist.")

# # # collection = db.get_or_create_collection("documents")


# # # #create a collection, If "documents" already exists, Chroma opens it. Otherwise, it creates it.
# # # collection = db.get_or_create_collection("documents")


# # # #connect chroma with Llamaindex
# # # # Think of StorageContext as telling LlamaIndex: "Whenever you create embeddings, store them in this Chroma collection."
# # # vector_store = ChromaVectorStore(
# # #     chroma_collection=collection
# # # )

# # # storage_context = StorageContext.from_defaults(
# # #     vector_store=vector_store
# # # )


# # # #Build the Index: Store embeddings in ChromaDB
# # # index = VectorStoreIndex(
# # #     nodes,
# # #     storage_context=storage_context,
# # #     embed_model=embed_model,
# # # )
# # # ''' Let's unpack it:
# # # nodes → the chunks you created.
# # # embed_model → converts each chunk into a vector.
# # # storage_context → tells LlamaIndex where to save those vectors.

# # # Under the hood, LlamaIndex loops through your nodes like this:
# # # for node in nodes:
# # #     embedding = embed(node.text)
# # #     save_to_chromadb(node, embedding)

# # # You don't have to write that loop yourself—that's the power of using a framework. '''


# # # print("✅ Index successfully created!")





# # # import os
# # # import chromadb

# # # from llama_index.core import Document
# # # from llama_index.core.node_parser import SentenceSplitter
# # # from llama_index.core import VectorStoreIndex
# # # from llama_index.core import StorageContext

# # # from llama_index.vector_stores.chroma import ChromaVectorStore
# # # from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# # # from ocr_utils import extract_text_from_pdf
# # # from ocr_utils import extract_text_from_image


# # # documents = []

# # # folder = "data"

# # # for file in os.listdir(folder):

# # #     path = os.path.join(folder, file)

# # #     if file.lower().endswith(".pdf"):

# # #         print(f"Processing PDF : {file}")

# # #         text = extract_text_from_pdf(path)

# # #         documents.append(Document(text=text))

# # # print(f"\nLoaded {len(documents)} documents")


# # # parser = SentenceSplitter(
# # #     chunk_size=256,
# # #     chunk_overlap=40,
# # # )

# # # nodes = parser.get_nodes_from_documents(documents)

# # # print(f"Created {len(nodes)} nodes")


# # # embed_model = HuggingFaceEmbedding(
# # #     model_name="BAAI/bge-small-en-v1.5"
# # # )


# # # db = chromadb.PersistentClient(
# # #     path="./chroma_db"
# # # )


# # # # Delete old collection if it exists
# # # try:
# # #     db.delete_collection("documents")
# # # except:
# # #     pass


# # # collection = db.get_or_create_collection("documents")


# # # vector_store = ChromaVectorStore(
# # #     chroma_collection=collection
# # # )


# # # storage_context = StorageContext.from_defaults(
# # #     vector_store=vector_store
# # # )


# # # index = VectorStoreIndex(
# # #     nodes,
# # #     storage_context=storage_context,
# # #     embed_model=embed_model,
# # # )

# # # print("\n✅ Embeddings stored successfully.")





# # import os
# # import chromadb

# # from llama_index.core import Document
# # from llama_index.core.node_parser import SentenceSplitter
# # from llama_index.core import VectorStoreIndex
# # from llama_index.core import StorageContext

# # from llama_index.vector_stores.chroma import ChromaVectorStore
# # from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# # from ocr_utils import extract_text_from_pdf
# # from image_utils import (
# #     extract_images_from_pdf,
# #     describe_image_with_gemini,
# # )

# # # --------------------------------------------
# # # Load all documents
# # # --------------------------------------------

# # documents = []

# # folder = "data"

# # for file in os.listdir(folder):

# #     if not file.lower().endswith(".pdf"):
# #         continue

# #     pdf_path = os.path.join(folder, file)

# #     print(f"\nProcessing PDF: {file}")

# #     # ----------------------------------------
# #     # Step 1 : Extract text (Normal + OCR)
# #     # ----------------------------------------

# #     text = extract_text_from_pdf(pdf_path)

# #     # ----------------------------------------
# #     # Step 2 : Extract images
# #     # ----------------------------------------

# #     image_paths = extract_images_from_pdf(pdf_path)

# #     print(f"Found {len(image_paths)} images")

# #     image_descriptions = []

# #     for image_path in image_paths:

# #         print(f"Describing {os.path.basename(image_path)}")

# #         try:

# #             description = describe_image_with_gemini(image_path)

# #             image_descriptions.append(
# #                 f"\n\nIMAGE DESCRIPTION:\n{description}"
# #             )

# #         except Exception as e:

# #             print(f"Gemini failed: {e}")

# #         finally:

# #         # Delete temporary image
# #             if os.path.exists(image_path):
# #                 os.remove(image_path)
# #                 print(f"Deleted {os.path.basename(image_path)}")

# #     # ----------------------------------------
# #     # Step 3 : Merge everything
# #     # ----------------------------------------

# #     complete_document = (
# #         text
# #         + "\n\n"
# #         + "\n\n".join(image_descriptions)
# #     )

# #     documents.append(
# #         Document(text=complete_document)
# #     )

# # print(f"\nLoaded {len(documents)} documents")

# # # --------------------------------------------
# # # Chunking
# # # --------------------------------------------

# # parser = SentenceSplitter(
# #     chunk_size=256,
# #     chunk_overlap=40,
# # )

# # nodes = parser.get_nodes_from_documents(documents)

# # print(f"Created {len(nodes)} nodes")

# # # --------------------------------------------
# # # Embedding model
# # # --------------------------------------------

# # embed_model = HuggingFaceEmbedding(
# #     model_name="BAAI/bge-small-en-v1.5"
# # )

# # # --------------------------------------------
# # # ChromaDB
# # # --------------------------------------------

# # db = chromadb.PersistentClient(
# #     path="./chroma_db"
# # )

# # try:
# #     db.delete_collection("documents")
# #     print("Old collection deleted.")
# # except:
# #     pass

# # collection = db.get_or_create_collection("documents")

# # vector_store = ChromaVectorStore(
# #     chroma_collection=collection
# # )

# # storage_context = StorageContext.from_defaults(
# #     vector_store=vector_store
# # )

# # # --------------------------------------------
# # # Build Index
# # # --------------------------------------------

# # VectorStoreIndex(
# #     nodes=nodes,
# #     storage_context=storage_context,
# #     embed_model=embed_model,
# # )

# # print("\n✅ Embeddings stored successfully.")





# # import os
# # import chromadb

# # from llama_index.core import Document
# # from llama_index.core.node_parser import SentenceSplitter
# # from llama_index.core import VectorStoreIndex
# # from llama_index.core import StorageContext

# # from llama_index.vector_stores.chroma import ChromaVectorStore
# # from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# # from ocr_utils import (
# #     extract_text_from_pdf,
# #     extract_text_from_image,
# # )

# # from image_utils import (
# #     extract_images_from_pdf,
# #     describe_image_with_gemini,
# # )

# # # =====================================================
# # # LOAD DOCUMENTS
# # # =====================================================

# # documents = []

# # folder = "data"

# # for file in os.listdir(folder):

# #     path = os.path.join(folder, file)

# #     # =====================================================
# #     # PDF FILES
# #     # =====================================================

# #     if file.lower().endswith(".pdf"):

# #         print(f"\nProcessing PDF: {file}")

# #         # Extract text (normal + OCR)
# #         text = extract_text_from_pdf(path)

# #         # Extract images
# #         image_paths = extract_images_from_pdf(path)

# #         print(f"Found {len(image_paths)} images")

# #         image_descriptions = []

# #         for image_path in image_paths:

# #             print(f"Describing {os.path.basename(image_path)}")

# #             try:
# #                 description = describe_image_with_gemini(image_path)

# #                 image_descriptions.append(
# #                     f"\n\nIMAGE DESCRIPTION:\n{description}"
# #                 )

# #             except Exception as e:
# #                 print(f"Gemini failed: {e}")

# #             finally:
# #                 if os.path.exists(image_path):
# #                     os.remove(image_path)
# #                     print(f"Deleted {os.path.basename(image_path)}")

# #         # Merge text + image descriptions
# #         complete_document = (
# #             text +
# #             "\n\n" +
# #             "\n\n".join(image_descriptions)
# #         )

# #         documents.append(
# #             Document(
# #                 text=complete_document,
# #                 metadata={
# #                     "filename": file,
# #                     "type": "pdf"
# #                 }
# #             )
# #         )

# #     # =====================================================
# #     # IMAGE FILES
# #     # =====================================================

# #     elif file.lower().endswith((".jpg", ".jpeg", ".png")):

# #         print(f"\nProcessing Image: {file}")

# #         text = extract_text_from_image(path)

# #         documents.append(
# #             Document(
# #                 text=text,
# #                 metadata={
# #                     "filename": file,
# #                     # "type": "image"
# #                 }
# #             )
# #         )

# # print(f"\nLoaded {len(documents)} documents")

# # # =====================================================
# # # CHUNKING
# # # =====================================================

# # parser = SentenceSplitter(
# #     chunk_size=256,
# #     chunk_overlap=40,
# # )

# # nodes = parser.get_nodes_from_documents(documents)

# # print(f"Created {len(nodes)} nodes")

# # # =====================================================
# # # EMBEDDING MODEL
# # # =====================================================

# # embed_model = HuggingFaceEmbedding(
# #     model_name="BAAI/bge-small-en-v1.5"
# # )

# # # =====================================================
# # # CHROMADB
# # # =====================================================

# # db = chromadb.PersistentClient(
# #     path="./chroma_db"
# # )

# # try:
# #     db.delete_collection("documents")
# #     print("Old collection deleted.")
# # except:
# #     pass

# # collection = db.get_or_create_collection("documents")

# # vector_store = ChromaVectorStore(
# #     chroma_collection=collection
# # )

# # storage_context = StorageContext.from_defaults(
# #     vector_store=vector_store
# # )

# # # =====================================================
# # # BUILD INDEX
# # # =====================================================

# # VectorStoreIndex(
# #     nodes=nodes,
# #     storage_context=storage_context,
# #     embed_model=embed_model,
# # )

# # print("\n✅ Embeddings stored successfully.")



# import os
# # import chromadb

# from document_parser import parse_document
# from chunking import create_nodes
# from embedding import embed_model

# from llama_index.core import StorageContext
# from llama_index.core import VectorStoreIndex

# # from llama_index.vector_stores.chroma import ChromaVectorStore

# #new
# from qdrant_client import QdrantClient
# from llama_index.vector_stores.qdrant import QdrantVectorStore


# # ==========================================================
# # Configuration
# # ==========================================================

# DATA_FOLDER = "data"

# SUPPORTED_FILES = (
#     ".pdf",
#     ".docx",
#     ".pptx",
#     ".xlsx",
#     ".html",
#     ".md",
#     ".png",
#     ".jpg",
#     ".jpeg",
# )

# # ==========================================================
# # Read Documents
# # ==========================================================

# nodes = []

# for filename in os.listdir(DATA_FOLDER):

#     filepath = os.path.join(DATA_FOLDER, filename)

#     extension = os.path.splitext(filename)[1].lower()

#     if extension not in SUPPORTED_FILES:
#         continue

#     print(f"\nProcessing {filename}")

#     try:

#         text = parse_document(filepath)

#         if not text.strip():

#             print("Skipped (empty document)")
#             continue

#         metadata = {
#             "filename": filename,
#             "extension": extension,
#         }

#         nodes.extend(
#             create_nodes(
#                 text=text,
#                 metadata=metadata,
#             )
#         )

#     except Exception as e:

#         print(f"Failed to process {filename}")
#         print(e)

# print(f"\nCreated {len(nodes)} nodes")

# # ==========================================================
# # Connect ChromaDB
# # ==========================================================

# db = chromadb.PersistentClient(
#     path="./chroma_db"
# )

# try:

#     db.delete_collection("documents")
#     print("Old collection deleted.")

# except:

#     pass

# collection = db.get_or_create_collection(
#     "documents"
# )

# vector_store = ChromaVectorStore(
#     chroma_collection=collection
# )

# storage_context = StorageContext.from_defaults(
#     vector_store=vector_store
# )

# # ==========================================================
# # Build Vector Index
# # ==========================================================

# VectorStoreIndex(
#     nodes=nodes,
#     storage_context=storage_context,
#     embed_model=embed_model,
# )

# print("\n✅ Embeddings stored successfully.")




# import os

# from document_parser import parse_document
# from chunking import create_nodes
# from embedding import embed_model

# from llama_index.core import StorageContext
# from llama_index.core import VectorStoreIndex

# from qdrant_client import QdrantClient
# from llama_index.vector_stores.qdrant import QdrantVectorStore


# # ==========================================================
# # CONFIGURATION
# # ==========================================================

# DATA_FOLDER = "data"

# QDRANT_PATH = "./qdrant_db"
# COLLECTION_NAME = "documents"

# SUPPORTED_FILES = (
#     ".pdf",
#     ".docx",
#     ".pptx",
#     ".xlsx",
#     ".html",
#     ".md",
#     ".png",
#     ".jpg",
#     ".jpeg",
# )


# # ==========================================================
# # STEP 1 — READ DOCUMENTS
# # ==========================================================

# nodes = []

# print("\n" + "=" * 60)
# print("STARTING DOCUMENT INGESTION")
# print("=" * 60)

# for filename in os.listdir(DATA_FOLDER):

#     filepath = os.path.join(DATA_FOLDER, filename)

#     extension = os.path.splitext(filename)[1].lower()

#     # Skip unsupported files
#     if extension not in SUPPORTED_FILES:
#         continue

#     print(f"\nProcessing: {filename}")

#     try:

#         # --------------------------------------------------
#         # Extract text
#         # --------------------------------------------------

#         text = parse_document(filepath)

#         if not text or not text.strip():

#             print("⚠️ Skipped: document produced no text.")
#             continue

#         print(f"Extracted {len(text)} characters")

#         # --------------------------------------------------
#         # Metadata
#         # --------------------------------------------------

#         metadata = {
#             "filename": filename,
#             "extension": extension,
#         }

#         # --------------------------------------------------
#         # Chunk document
#         # --------------------------------------------------

#         document_nodes = create_nodes(
#             text=text,
#             metadata=metadata,
#         )

#         print(f"Created {len(document_nodes)} chunks")

#         nodes.extend(document_nodes)

#     except Exception as e:

#         print(f"❌ Failed to process {filename}")
#         print(f"Error: {e}")


# # ==========================================================
# # CHECK WHETHER NODES WERE CREATED
# # ==========================================================

# print("\n" + "=" * 60)
# print(f"TOTAL NODES CREATED: {len(nodes)}")
# print("=" * 60)

# if not nodes:

#     print(
#         "\n❌ No nodes were created."
#         "\n\nThis means the problem occurred BEFORE Qdrant."
#         "\nCheck document_parser.py / OCR / Docling / input files."
#     )

#     raise SystemExit(1)


# # ==========================================================
# # STEP 2 — CONNECT TO QDRANT
# # ==========================================================

# print("\nConnecting to Qdrant...")

# # Local persistent Qdrant database.
# #
# # This creates:
# #
# #     ./qdrant_db
# #
# # Qdrant will store the vectors there.
# #
# # No Docker is required for this local setup.

# qdrant_client = QdrantClient(
#     path=QDRANT_PATH
# )

# print("✅ Qdrant client connected")


# # ==========================================================
# # STEP 3 — DELETE OLD COLLECTION
# # ==========================================================

# # During development, we want a clean collection every time
# # vector_store.py is executed.
# #
# # IMPORTANT:
# # Later, when your ingestion pipeline is stable,
# # we should remove this deletion logic so documents
# # are not re-embedded every time.

# try:

#     if qdrant_client.collection_exists(COLLECTION_NAME):

#         qdrant_client.delete_collection(
#             collection_name=COLLECTION_NAME
#         )

#         print(
#             f"🗑️ Deleted old Qdrant collection: "
#             f"{COLLECTION_NAME}"
#         )

# except Exception as e:

#     print(f"⚠️ Could not delete old collection: {e}")


# # ==========================================================
# # STEP 4 — CREATE QDRANT VECTOR STORE
# # ==========================================================

# vector_store = QdrantVectorStore(
#     client=qdrant_client,
#     collection_name=COLLECTION_NAME,
# )

# print("✅ QdrantVectorStore created")


# # ==========================================================
# # STEP 5 — CREATE LLAMAINDEX STORAGE CONTEXT
# # ==========================================================

# storage_context = StorageContext.from_defaults(
#     vector_store=vector_store
# )

# print("✅ StorageContext created")


# # ==========================================================
# # STEP 6 — CREATE VECTOR INDEX
# # ==========================================================

# print("\nCreating embeddings and storing vectors...")

# index = VectorStoreIndex(
#     nodes=nodes,
#     storage_context=storage_context,
#     embed_model=embed_model,
# )

# print("\n" + "=" * 60)
# print("✅ INGESTION SUCCESSFUL")
# print("=" * 60)

# print(f"Documents/chunks processed : {len(nodes)}")
# print(f"Vector database            : Qdrant")
# print(f"Collection                 : {COLLECTION_NAME}")
# print(f"Storage path               : {QDRANT_PATH}")

# print("\n✅ Embeddings stored successfully in Qdrant.")


# # ==========================================================
# # STEP 7 — VERIFY COLLECTION
# # ==========================================================

# try:

#     collection_info = qdrant_client.get_collection(
#         collection_name=COLLECTION_NAME
#     )

#     print("\n" + "=" * 60)
#     print("QDRANT COLLECTION VERIFICATION")
#     print("=" * 60)

#     print(
#         f"Collection: {COLLECTION_NAME}"
#     )

#     print(
#         f"Vectors stored: "
#         f"{collection_info.points_count}"
#     )

#     print("\n✅ Qdrant verification successful.")

# except Exception as e:

#     print("\n⚠️ Could not verify Qdrant collection.")
#     print(f"Error: {e}")


# # ==========================================================
# # CLEANUP
# # ==========================================================

# qdrant_client.close()

# print("\nDone.")




import os

from document_parser import parse_document
from chunking import create_nodes
from embedding import embed_model

from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from llama_index.vector_stores.qdrant import QdrantVectorStore


# ==========================================================
# CONFIGURATION
# ==========================================================

DATA_FOLDER = "data"

QDRANT_PATH = "./qdrant_db"

COLLECTION_NAME = "documents"

SUPPORTED_FILES = (
    ".pdf",
    ".docx",
    ".pptx",
    ".xlsx",
    ".html",
    ".md",
    ".png",
    ".jpg",
    ".jpeg",
)


# ==========================================================
# START
# ==========================================================

print("\n" + "=" * 60)
print("STARTING DOCUMENT INGESTION")
print("=" * 60)


# ==========================================================
# READ DOCUMENTS + CREATE NODES
# ==========================================================

nodes = []


for filename in os.listdir(DATA_FOLDER):

    filepath = os.path.join(DATA_FOLDER, filename)

    extension = os.path.splitext(filename)[1].lower()

    if extension not in SUPPORTED_FILES:
        continue

    print(f"\nProcessing: {filename}")

    try:

        # --------------------------------------------------
        # Extract text
        # --------------------------------------------------

        text = parse_document(filepath)

        if not text or not text.strip():

            print("Skipped: empty document")
            continue

        # --------------------------------------------------
        # Metadata
        # --------------------------------------------------

        metadata = {
            "filename": filename,
            "extension": extension,
        }

        # --------------------------------------------------
        # Chunk document
        # --------------------------------------------------

        document_nodes = create_nodes(
            text=text,
            metadata=metadata,
        )

        nodes.extend(document_nodes)

        print(f"Created {len(document_nodes)} chunks")

    except Exception as e:

        print(f"❌ Failed to process {filename}")
        print(f"Error: {e}")


# ==========================================================
# NODE SUMMARY
# ==========================================================

print("\n" + "=" * 60)
print(f"TOTAL NODES CREATED: {len(nodes)}")
print("=" * 60)


if not nodes:

    print("\n❌ No nodes were created.")
    print("Nothing will be inserted into Qdrant.")
    raise SystemExit(1)


# ==========================================================
# CREATE QDRANT CLIENT
# ==========================================================

print("\nConnecting to Qdrant...")

qdrant_client = QdrantClient(
    path=QDRANT_PATH
)

print("✅ Qdrant client connected")


# ==========================================================
# DETERMINE VECTOR DIMENSION
# ==========================================================

print("\nChecking embedding dimension...")

test_embedding = embed_model.get_text_embedding(
    "test embedding"
)

VECTOR_SIZE = len(test_embedding)

print(f"Embedding dimension: {VECTOR_SIZE}")


# ==========================================================
# CREATE / RECREATE QDRANT COLLECTION
# ==========================================================

print(f"\nPreparing collection: {COLLECTION_NAME}")

existing_collections = qdrant_client.get_collections()

collection_exists = any(
    collection.name == COLLECTION_NAME
    for collection in existing_collections.collections
)


if collection_exists:

    print(f"Existing collection '{COLLECTION_NAME}' found.")

    print("Deleting old collection...")

    qdrant_client.delete_collection(
        collection_name=COLLECTION_NAME
    )

    print("✅ Old collection deleted.")


# ----------------------------------------------------------
# Create fresh collection
# ----------------------------------------------------------

qdrant_client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=VECTOR_SIZE,
        distance=Distance.COSINE,
    ),
)

print("✅ Qdrant collection created")


# ==========================================================
# CONNECT QDRANT TO LLAMAINDEX
# ==========================================================

vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name=COLLECTION_NAME,
)


storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)


# ==========================================================
# BUILD VECTOR INDEX
# ==========================================================

print("\nCreating embeddings and storing them in Qdrant...")

index = VectorStoreIndex(
    nodes=nodes,
    storage_context=storage_context,
    embed_model=embed_model,
)


# ==========================================================
# VERIFY
# ==========================================================

collection_info = qdrant_client.get_collection(
    collection_name=COLLECTION_NAME
)

print("\n" + "=" * 60)
print("✅ INGESTION COMPLETED SUCCESSFULLY")
print("=" * 60)

print(f"Collection: {COLLECTION_NAME}")
print(f"Vector dimension: {VECTOR_SIZE}")
print(f"Points stored: {collection_info.points_count}")
print("=" * 60)

qdrant_client.close()