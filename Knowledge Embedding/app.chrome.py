import streamlit as st
from icecream import ic
from langchain_chroma_1 import chromaStore

store = None


def generate_response(message: str) -> str:
    docs = store.similarity_search(message,3)
    # result = store.show_docs(docs)
    result = store.ai_result(message, docs)    
    print(f"result: {result}")
    return result

# 1. Build an app with streamlit
def main():
    st.set_page_config(
        page_title="Customer response generator", page_icon=":bird:")

    st.header("Customer response generator :bird:")
    message = st.text_area("customer message")

    if message:
        st.write("Generating best practice message...")
        result = generate_response(message)
        st.info(result['response'])
#     result = generate_response("""
#     ik zie deze regel in de log, wat betekent dit?
    
# I 01/01/1970 00:08:28 {main} [SerialPortTransport./dev/ttyXRUSB4]: >req[eNo0027-09.01-900001-000]:01;ati|3E;
# I 01/01/1970 00:08:28 {Thread-62} [SerialPortTransport./dev/ttyXRUSB4]: resp[eNo0027-09.01-900001-000]01:OK;> eVCC_V3 Firmware 110.8.3 256d3|B1;
#                                """)
#     ic(result['response'])

if __name__ == '__main__':
    store = chromaStore("demo")
    store.clear_collection()
    store.embed_from_markdown("EVCC_Firmware_issue.md")
    store.embed_from_markdown("kwh.md")
    main()