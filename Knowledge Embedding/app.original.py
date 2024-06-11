import streamlit as st
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

# 1. Vectorise the sales response csv data
loader = CSVLoader(file_path="demo.csv")
documents = loader.load()

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(documents, embeddings)

# 2. Function for similarity search


def retrieve_info(query):
    similar_response = db.similarity_search(query, k=3)

    page_contents_array = [doc.page_content for doc in similar_response]

    # print(page_contents_array)

    return page_contents_array


# 3. Setup LLMChain & prompts
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")

template = """
Je bent een eersteklas techneut gespecialseert in ondersteuning van monteurs.
Ik zal een vraag van een monteur met je delen en je geeft mij het beste antwoord dat ik naar deze monteur moet sturen, gebaseerd op eerdere best practices. Je volgt ALLE onderstaande regels:

1/ Het antwoord moet zeer vergelijkbaar of zelfs identiek zijn aan de eerdere best practices, in termen van lengte, toon, logische argumenten en andere details.

2/ Als de best practices niet relevant zijn, probeer dan de stijl van de best practices na te bootsen in het bericht aan de monteur.

Hieronder staat een bericht dat ik van de monteur heb ontvangen:
{message}

Hier is een lijst van best practices van hoe we normaal reageren op monteurs in vergelijkbare situaties:
{best_practice}

Schrijf alsjeblieft het beste antwoord dat ik naar deze monteur moet sturen
"""

prompt = PromptTemplate(
    input_variables=["message", "best_practice"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)


# 4. Retrieval augmented generation
def generate_response(message):
    best_practice = retrieve_info(message)
    response = chain.run(message=message, best_practice=best_practice)
    return response


# 5. Build an app with streamlit
def main():
    st.set_page_config(
        page_title="Customer response generator", page_icon=":bird:")

    st.header("Customer response generator :bird:")
    message = st.text_area("customer message")

    if message:
        st.write("Generating best practice message...")

        result = generate_response(message)

        st.info(result)


if __name__ == '__main__':
    main()