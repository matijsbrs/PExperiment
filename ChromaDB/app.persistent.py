# 19-05-2024 
# Start learning ChromaDB
# author: Matijs Behrens
# learning steps from trychroma.com


# pip requirements
# pip install chromadb icecream

import chromadb
from icecream import ic

client = chromadb.PersistentClient(path='./my_chroma_db')


client.heartbeat()
# client.delete_collection('my_collection')
def create_collection(client, colelction_name='my_collection'):
    collection = client.create_collection(colelction_name)

    return collection

def add_documents(collection):
    collection.add(
        documents=[
            "This is a document about pineapple",
            "This is a document about oranges",
            "This is a document about apples",	
        ],
        ids=["id1", "id2", "id3"],
        metadatas=[
            {"name": "fruit", "value": "pineapple"},
            {"name": "fruit", "value": "oranges"},
            {"name": "fruit", "value": "apples"}
        ]
    )

def update_documents(collection):
    collection.update(
        documents=[
            "This is a document about pineapple",
            "This is a document about oranges",
            "This is a document about apples",	
        ],
        ids=["id1", "id2", "id3"],
        metadatas=[
            {"name": "fruit", "value": "pineapple"},
            {"name": "fruit", "value": "oranges"},
            {"name": "fruit", "value": "apples"}
        ]
    )

def load_collection(client, collection_name='my_collection'):
    collection = client.get_collection(collection_name)

    return collection


def show_statistics(collection):
    stats = collection.count()
    ic(f"Size: {stats}")

try:
    collection =load_collection(client)
    ic("Loaded collection")
except ValueError:
    ic("collection not found, creating a new one.")
    collection = create_collection(client)
    add_documents(collection)
    
# add_documents(collection)

show_statistics(collection)


results = collection.query(
    query_texts=["This is a query document about Nederland"], # Chroma will embed this for you
    include=['distances', 'metadatas','documents'],
    n_results=10,
    where={"metadata_field": "value"},
    # where_document={"$contains":"about"}
)
ic(results)

# ic(collection.peek())