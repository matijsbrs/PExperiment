import streamlit as st
from icecream import ic
from langchain_chroma_1 import chromaStore
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

store = None

def calculate_cosine_similarity(query_embedding, doc_embedding):
    query_embedding = query_embedding.reshape(1, -1)
    doc_embedding = doc_embedding.reshape(1, -1)
    similarity = cosine_similarity(query_embedding, doc_embedding)
    return similarity[0][0]

def generate_response(message: str, filters: dict):
    docs = store.similarity_search_with_filters(message, 10, filters)
    query_embedding = store.embed_text(message)
    
    # ic(docs)
    scored_docs = []
    print("size: ", len(docs['distances'][0]))
    for doc in range(0,len(docs['distances'][0])):
        # similarity_score = calculate_cosine_similarity(query_embedding, doc_embedding)
        #scored_docs.append((doc, docs['distances'][0][index]))
        scored_doc = {
            "content": docs['documents'][0][doc],
            "distance": docs['distances'][0][doc],
            "metadata": docs['metadatas'][0][doc],
            "ids": docs['ids'][0][doc]
        }
        print(f"distance: {scored_doc['distance']}")
        scored_docs.append(scored_doc)
    
    
    # scored_docs.sort(key=lambda doc: doc['distance'])
    # top_docs = [doc for doc in scored_docs[:3]]
    top_docs = scored_docs[:3]
    # ic(scored_docs)
    if not top_docs:
        return {"response": "No relevant documents found.", "resources": []}
    
    result = store.ai_result(message, top_docs)
    used_resources = [doc['metadata'] for doc in top_docs]
    
    response = {"response": result['response'], "resources": used_resources, "documents": top_docs}
    ic(response)
    # print(f"response: {response}")
    return response

def main():
    st.set_page_config(page_title="Customer response generator", page_icon=":rocket:")
    st.header("Customer response generator :rocket:")
    
    message = st.text_area("Customer message")
    
    # Metadata filters
    st.sidebar.header("Filters")
    tag_filter = st.sidebar.text_input("Tag")
    author_filter = st.sidebar.text_input("Author")
    
    filters = {}
    if tag_filter:
        filters['tags'] = tag_filter
    if author_filter:
        filters['author'] = author_filter

    if message:
        st.write("Generating best practice message...")
        result = generate_response(message, filters)
        st.info(result['response'])
        
        st.write("Resources used:")
        for resource in result['resources']:
            st.write(resource)
        
        # st.write("Detailed Document Information:")
        # for doc in result:
        #     # file_path = doc['metadata']['name']
        #     # st.write(f"File Path: {file_path}")
        #     # st.write(f"Metadata: {doc['metadata']}")
        #     # st.write(f"[Open Document](http://localhost:8502/?file={file_path})")  # Link naar het aparte Streamlit-bestand
        #     st.write("---")

if __name__ == '__main__':
    store = chromaStore("demo")
    store.embed_from_markdown("EVCC_Firmware_issue.md")
    store.embed_from_markdown("kwh.md")
    main()
