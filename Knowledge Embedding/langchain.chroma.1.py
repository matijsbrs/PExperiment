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


# load the document and split it into chunks 
def load_text_document(file_path):
    # load the document and split it into chunks
    loader = TextLoader(file_path)
    documents = loader.load()

    # split it into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    return docs

docs = load_text_document("demo.md")

# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# load it into Chroma
db = Chroma.from_documents(docs, embedding_function)
# show the number of documents in the collection
print("There are", db._collection.count(), "in the collection")

# query it
query = "Wat zijn de top 3 kwaliteiten van matijs?"
docs = db.similarity_search(query)

# prepare the llm model
llm_mistral = ChatOllama(model="mistral:7b", temperature=0.3, max_tokens=200, base_url="http://192.168.2.61:11434")
template = """
Je bent een eersteklas onderzoeker. gespecialiseerd in het vinden van informatie over een onderwerp.
Je krijgt een vraag van een student en je moet het antwoord geven op basis van de informatie die je hebt gevonden.
Je volgt ALLE onderstaande regels:

1. Het antwoord moet zeer vergelijkbaar of zelfs identiek zijn aan de eerdere best practices, in termen van lengte, toon, logische argumenten en andere details.
2. Als de best practices niet relevant zijn, probeer dan de stijl van de best practices na te bootsen in het bericht aan de monteur.
3. Reageer in het Nederlands.

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

# using langchain expressive language chain syntax
# see: /docs/concepts/#langchain-expression-language-lcel

models = [
    {"name": "mistral", "model": llm_mistral},
]

for llm in models:
    chain = prompt | llm['model'] | StrOutputParser()
    combined = "\n".join([doc.page_content for doc in docs])
    chain_query = {"query": query, "relavant_info": combined}
    print( f"""
Result for model: {llm['name']}
----
{chain.invoke(chain_query)}
----
""")