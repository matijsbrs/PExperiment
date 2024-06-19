# import
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_openai import ChatOpenAI
from langchain_text_splitters import CharacterTextSplitter

# LangChain supports many other chat models. Here, we're using Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from Markdown_loader_2 import parse_markdown

import chromadb

class chromaStore:
    
    collectionName = None
    collection = None
    cclient = None
    db = None

    def __init__(self, collectionName="demo"):
        self.collectionName = collectionName
        self.cclient = chromadb.PersistentClient()
        
        
    def clear_collection(self):
        self.collection = self.cclient.get_or_create_collection(self.collectionName)
        self.cclient.delete_collection(self.collectionName)
        self.collection = self.cclient.get_or_create_collection(self.collectionName)


    # load the document and split it into chunks 
    def load_text_document(self, file_path):
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
        self.db = Chroma(
            client=self.cclient,
            collection_name=self.collectionName,
            embedding_function=embedding_function,
        )

        collection = self.cclient.get_or_create_collection(self.collectionName)
        for i, doc in enumerate(docs):
            # print(f"Index: {i}, Document: {doc.page_content}")
            collection.add(ids=[f"id{i}"], documents=[doc.page_content])

        return self.db

    def embed_from_markdown(self, file_path):
        # load the document and split it into chunks
        chapters = parse_markdown(file_path)
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        # load it into Chroma
        # db = Chroma.from_documents(docs, embedding_function)
        self.db = Chroma(
            client=self.cclient,
            collection_name=self.collectionName,
            embedding_function=embedding_function,
        )

        self.collection = self.cclient.get_or_create_collection(self.collectionName)
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
            

            self.collection.add(
                documents=[chapter['content']],
                ids=[f"{source['name']}.{chapter['index']}"],
                metadatas=metadata
            )
            # print(f"Chapter: {chapter}")
            
        return self.db
    
    
    def similarity_search_with_score(self, query):
        return self.db.similarity_search_with_score(query)
    
    def similarity_search(self, query, n_results=10):
        return self.collection.query(
            query_texts=[f"{query}"],
            n_results=n_results,
            # where={"metadata_field": "is_equal_to_this"},
            # where_document={"$contains":"search_string"}
        )


    
    def show_docs(self, docs):
        # print the results from docs
        for doc in docs:
            document = doc
            print(f"{document}")

        # print(f"""
                
        # content:
        # {document.page_content}

        # metadata:
        # {document.metadata}

        # """)

    def ai_result(self, query, docs):
        # prepare the llm model
        # llm_mistral = ChatOllama(model="tinyllama:latest", temperature=0.3, max_tokens=400, base_url="http://192.168.2.61:11434")
        llm = ChatOpenAI(temperature=0.1, model="gpt-4o")

        

        template = """
        Je bent een eersteklas onderzoeker. gespecialiseerd in het vinden van informatie over een onderwerp.
        Je krijgt een vraag van een student en je moet het antwoord geven op basis van de informatie die je hebt gevonden.
        Je volgt ALLE onderstaande regels:

        1. Het antwoord moet zeer vergelijkbaar of zelfs identiek zijn aan de eerdere best practices, in termen van lengte, toon, logische argumenten en andere details.
        2. Als de best practices niet relevant zijn, probeer dan de stijl van de best practices na te bootsen in het bericht aan de monteur.
        3. Neem de lijst van relevante bronnen op in het antwoord.
        4. Reageer in het Nederlands.
        5. Formateer de tekst netjes in Markdown.

        Hieronder staat de onderzoeksvraag:
        {query}

        Hier is een lijst van gerelateerde informatie die je hebt gevonden:
        {relavant_info}

        Bronnen:
        {sources}

        Schrijf het beste antwoord waarvan jij denkt dat het de onderzoeksvraag beantwoord.
        """
        prompt = ChatPromptTemplate.from_template(template)

        # using langchain expressive language chain syntax
        # see: /docs/concepts/#langchain-expression-language-lcel
        
        chain = prompt | llm | StrOutputParser()
        # combined = "\n".join([doc[0].page_content for doc in docs])
        combined = "\n".join([doc for doc in docs['documents'][0]])
        sources = ""
        for source in docs['metadatas'][0]:
            sources += f"* {source['name']} - {source['index']} \n"


        chain_query = {"query": query, "relavant_info": combined, "sources": sources}

        llm_result = {
            "query": query,
            "database": docs,
            "referencs": sources,
            "response": chain.invoke(chain_query)
        }

        return  llm_result


