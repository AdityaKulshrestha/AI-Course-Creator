import os
import streamlit as st
from pdf_reader import pdf_reader, text_to_docs, embed_docs, search_docs, get_answer
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from utils import link_to_image

st.title("AI Course Creator")

openai_key = st.text_input("Enter your OpenAI key", type='password')
serpapi_key = st.text_input("Enter your SerperAPI key", type='password')

os.environ['OPENAI_API_KEY'] = openai_key
os.environ['SERPER_API_KEY'] = serpapi_key


title = st.text_input("Enter the title of your course")

if st.button("Submit"):
    # Loading the vectorstore db if exists
    if os.path.exists('./vector_db'):
        index = Chroma(persist_directory='./vector_db', embedding_function=OpenAIEmbeddings())
    else:
        text = pdf_reader('./PDFs/Motion_IX.pdf')
        processed_txt = text_to_docs(text)
        index = embed_docs(processed_txt)

    # topic = input("Enter your topic : ")
    sources = search_docs(index, title)
    print(sources)
    answer = get_answer(sources, title)
    st.markdown( link_to_image(answer['output_text']))




