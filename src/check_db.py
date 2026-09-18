# import chromadb

# client = chromadb.PersistentClient(path="./chroma_db")

# collection = client.get_collection("documents")

# print("Number of vectors:", collection.count())

# data = collection.get()

# print(len(data["ids"]))

# print(data["ids"][:10])

# import chromadb

# db = chromadb.PersistentClient(path="./chroma_db")
# collection = db.get_collection("documents")

# print("Number of vectors:", collection.count())

import chromadb

db = chromadb.PersistentClient(path="./chroma_db")
collection = db.get_collection("documents")

results = collection.get()

print("Vectors:", len(results["documents"]))

for i, doc in enumerate(results["documents"]):
    print("\n----------------")
    print("Chunk", i + 1)
    print("----------------")
    print(doc[:300])



