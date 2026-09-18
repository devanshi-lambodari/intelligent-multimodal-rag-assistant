# from llama_index.core import SimpleDirectoryReader
# from llama_index.core.node_parser import SentenceSplitter

# documents = SimpleDirectoryReader("data").load_data()

# splitter = SentenceSplitter(
#     chunk_size=700,
#     chunk_overlap=100
# )


# nodes = splitter.get_nodes_from_documents(documents)

# print(f"Number of documents: {len(documents)}")
# print(f"Number of nodes: {len(nodes)}")

# print("\nFirst node:\n")
# print(nodes[0].text)

# print("\nLength of first node:")
# print(len(nodes[0].text))


from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter


# ==========================================================
# Default chunker for prose documents
# ==========================================================

text_splitter = SentenceSplitter(
    chunk_size=700,
    chunk_overlap=100,
)


def create_nodes(text: str, metadata: dict):
    """
    Convert extracted text into LlamaIndex nodes.
    """

    document = Document(
        text=text,
        metadata=metadata,
    )

    return text_splitter.get_nodes_from_documents(
        [document]
    )