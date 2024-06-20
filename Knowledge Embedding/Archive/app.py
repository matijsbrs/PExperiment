import streamlit as st
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.llms import Ollama
from langchain_openai import OpenAI
from langchain_community.embeddings import GPT4AllEmbeddings

load_dotenv()

# 1. Vectorise the sales response csv data
loader = CSVLoader(file_path="demo.csv")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(documents)

# model_name = "all-MiniLM-L6-v2.gguf2.f16.gguf"
# gpt4all_kwargs = {'allow_download': 'True'}
# embeddings = GPT4AllEmbeddings(
#     model_name=model_name,
#     gpt4all_kwargs=gpt4all_kwargs,    
# )
from langchain.embeddings.openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()


vectorstore = Chroma.from_documents(documents=all_splits, embedding=embeddings)

# 2. Function for similarity search


def retrieve_info(query):
    similar_response = vectorstore.similarity_search(query, k=3)

    page_contents_array = [doc.page_content for doc in similar_response]

    # print(page_contents_array)

    return page_contents_array


# 3. Setup LLMChain & prompts
# llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")
# llm = Ollama(model="qwen:0.5b", temperature=0.1, base_url="http://192.168.2.61:11434")
llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0.1)

template = """
You are a world class business development representative. 
I will share a prospect's message with you and you will give me the best answer that 
I should send to this prospect based on past best practies, 
and you will follow ALL of the rules below:

1/ Response should be very similar or even identical to the past best practies, 
in terms of length, ton of voice, logical arguments and other details

2/ If the best practice are irrelevant, then try to mimic the style of the best practice to prospect's message

Below is a message I received from the prospect:
{message}

Here is a list of best practies of how we normally respond to prospect in similar scenarios:
{best_practice}

Please write the best response that I should send to this prospect:
"""

prompt = PromptTemplate(
    input_variables=["message", "best_practice"],
    template=template
)

# chain = RunnableSequence(llm=llm, prompt=prompt)
chain = llm | prompt


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