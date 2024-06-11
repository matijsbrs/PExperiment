# import
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_text_splitters import CharacterTextSplitter

# LangChain supports many other chat models. Here, we're using Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from Markdown_loader_2 import parse_markdown

import chromadb

cclient = chromadb.PersistentClient()
collection = cclient.get_or_create_collection("demo")
cclient.delete_collection("demo")
collection = cclient.get_or_create_collection("demo")

# collection.add(ids=["1", "2", "3"], documents=["a", "b", "c"])

# load the document and split it into chunks 
def load_text_document(file_path, persistent_client, collection_name="demo"):
    # load the document and split it into chunks
    loader = TextLoader(file_path)
    documents = loader.load()

    # split it into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    # create the open-source embedding function
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # load it into Chroma
    # db = Chroma.from_documents(docs, embedding_function)
    db = Chroma(
        client=persistent_client,
        collection_name=collection_name,
        embedding_function=embedding_function,
    )

    collection = persistent_client.get_or_create_collection(collection_name)
    for i, doc in enumerate(docs):
        # print(f"Index: {i}, Document: {doc.page_content}")
        collection.add(ids=[f"id{i}"], documents=[doc.page_content])

    return db

def embed_from_markdown(file_path, persistent_client, collection_name="demo"):
    # load the document and split it into chunks
    chapters = parse_markdown(file_path)
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # load it into Chroma
    # db = Chroma.from_documents(docs, embedding_function)
    db = Chroma(
        client=persistent_client,
        collection_name=collection_name,
        embedding_function=embedding_function,
    )

    collection = persistent_client.get_or_create_collection(collection_name)
    for element in chapters['chapters']:
        chapter = element['chapter']
        source = element['source']
        tags = []
        related = []
        for tag in source['tags']:
            tags.append({"tag": tag})
        for rel in source['related']:
            related.append({"related": rel})

        metadata = [{
            "name": source['name'],
            "author": source['author'],
            "date": source['date'],
            "index": chapter['index'],
        }]
        

        collection.add(
            documents=[chapter['content']],
            ids=[f"{source['name']}.{chapter['index']}"],
            metadatas=metadata
        )
        # print(f"Chapter: {chapter}")
        
    return db
 


# db = load_text_document("demo.md", cclient, "demo")
db = embed_from_markdown("demo.md", cclient, "demo")

# dbmd = embed_from_markdown("demo.md")

# show the number of documents in the collection
print("There are", db._collection.count(), "in the collection")

# query it
query = "Beschrijf in het kort wat een Transformar is"
# docs = db.similarity_search(query)
docs = db.similarity_search_with_score(query)

# prepare the llm model
llm_mistral = ChatOllama(model="mistral:7b", temperature=0.3, max_tokens=400, base_url="http://192.168.2.61:11434")
template = """
Je bent een eersteklas onderzoeker. gespecialiseerd in het vinden van informatie over een onderwerp.
Je krijgt een vraag van een student en je moet het antwoord geven op basis van de informatie die je hebt gevonden.
Je volgt ALLE onderstaande regels:

1. Het antwoord moet zeer vergelijkbaar of zelfs identiek zijn aan de eerdere best practices, in termen van lengte, toon, logische argumenten en andere details.
2. Als de best practices niet relevant zijn, probeer dan de stijl van de best practices na te bootsen in het bericht aan de monteur.
3. Reageer in het Nederlands.
4. Formateer de tekst netjes in Markdown.

Hieronder staat de onderzoeksvraag:
{query}

Hier is een lijst van gerelateerde informatie die je hebt gevonden:
{relavant_info}

Schrijf het beste antwoord waarvan jij denkt dat het de onderzoeksvraag beantwoord.
"""
prompt = ChatPromptTemplate.from_template(template)

# print results
# print(f"""\n
# ####
# # Result:
# {docs[0].page_content}
# ####
# \n""")

# print the results from docs
for doc in docs:
    document, score = doc
    print(f"""
          
content:
{document.page_content}

metadata:
{document.metadata}

score:
{score}
          """)

# using langchain expressive language chain syntax
# see: /docs/concepts/#langchain-expression-language-lcel

models = [
    {"name": "mistral", "model": llm_mistral},
]

for llm in models:
    chain = prompt | llm['model'] | StrOutputParser()
    
    combined = "\n".join([doc[0].page_content for doc in docs])
    chain_query = {"query": query, "relavant_info": combined}
    print( f"""
Result for model: {llm['name']}
++++ Bron data:
{combined}
++++

---- Model response:
{chain.invoke(chain_query)}
----
""")