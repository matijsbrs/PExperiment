# import
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import CharacterTextSplitter

# LangChain supports many other chat models. Here, we're using Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from Markdown_loader_2 import parse_markdown

import os
import chromadb
from icecream import ic

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
        """
        Load a text document into the database. and check if the document is already in the database.

        Args:
            file_path (str): The path to the text document.

        Returns:
            None

        Raises:
            None
        """
        loader = TextLoader(file_path)
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        self.db = Chroma(
            client=self.cclient,
            collection_name=self.collectionName,
            embedding_function=embedding_function,
        )

        collection = self.collection
        file_hash = self.compute_file_hash(file_path)
        existing_docs = collection.get_documents({"file_hash": file_hash})
        
        if existing_docs:
            print(f"File {file_path} is already in the database. Skipping.")
            return
        
        print(f"File {file_path} is not in the database. Adding.")
        for doc in docs:
            doc["metadata"]["file_path"] = file_path
            doc["metadata"]["file_hash"] = file_hash
            doc["metadata"]["file_name"] = os.path.basename(file_path)
            collection.add_documents(documents=[doc])

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
    
    def filter_documents_by_metadata(self, metadata_filter):
        return self.collection.get_documents(metadata_filter)

    def similarity_search_with_filters(self, query, num_results=3, metadata_filter=None):
        docs = self.similarity_search(query, num_results)
        
        if metadata_filter:
            docs = [doc for doc in docs if all(item in doc['metadata'].items() for item in metadata_filter.items())]
        return docs

    def similarity_search(self, query, n_results=10):
        return self.collection.query(
            query_texts=[f"{query}"],
            n_results=n_results,
            # include=["distances"],
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

    def embed_text(self, text):
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        return embedding_function.embed_query(text)

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

        combined = "\n".join([doc['content'] for doc in docs])
        # combined = ""
        # for doc in docs['documents']:
        #     combined += doc['content']

        # ic(docs)
        # combined = "combi!"

        sources = ""
        for source in docs:
            sources += f"* {source['metadata']['name']} - {source['metadata']['index']} \n"
            # sources += f"* {source['name']} - {source['index']} \n"


        chain_query = {"query": query, "relavant_info": combined, "sources": sources}

        llm_result = {
            "query": query,
            "database": docs,
            "referencs": sources,
            "response": chain.invoke(chain_query)
        }

        return  llm_result


