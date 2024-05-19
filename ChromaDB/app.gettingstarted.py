# 19-05-2024 
# Start learning ChromaDB
# author: Matijs Behrens
# learning steps from trychroma.com


# pip requirements
# pip install chromadb icecream

import chromadb
from icecream import ic
chroma_client = chromadb.Client()

collection = chroma_client.create_collection('my_collection')

collection.add(
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges",
        "This is a document about dikes",	
    ],
    ids=["id1", "id2", "id3"]
)

results = collection.query(
    query_texts=["This is a query document about Nederland"], # Chroma will embed this for you
    n_results=2 # how many results to return
)
print(results)

ic(results)