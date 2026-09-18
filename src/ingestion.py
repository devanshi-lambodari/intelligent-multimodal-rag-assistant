# from llama_index.core import SimpleDirectoryReader   #It only loads documents.

# documents = SimpleDirectoryReader("data").load_data()
# '''
# The librarian knows:
# "My job is to look inside the data/ folder."
# Nothing has been read yet.

# This tells the librarian:
# "Now actually read every supported file."
# Now LlamaIndex:
# opens each PDF
# extracts the text
# creates Document objects
# '''

# # print(documents)
# print(type(documents))
# print(type(documents[0]))
# print(documents[0].text[:1000])


from llama_index.core import SimpleDirectoryReader

docs = SimpleDirectoryReader("data").load_data()

print(type(docs))
print(type(docs[0]))

print("\nFirst 500 chars:\n")
print(docs[0].text[:500])

print(type(docs[0]))

print("\n========== METADATA ==========")
print(docs[0].metadata)

print("\n========== TEXT LENGTH ==========")
print(len(docs[0].text))

print("\n========== FIRST 300 CHARACTERS ==========")
print(docs[0].text[:300])

#Notice that embeddings are created from nodes, not directly from documents.


