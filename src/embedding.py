# from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# embed_model = HuggingFaceEmbedding(
#     model_name="BAAI/bge-small-en-v1.5"
# )

# text = "Python is an amazing programming language."

# embedding = embed_model.get_text_embedding(text)

# print(type(embedding))
# print(len(embedding))

# print("\nFirst 10 numbers:")
# print(embedding[:10])


from llama_index.embeddings.huggingface import HuggingFaceEmbedding


embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)