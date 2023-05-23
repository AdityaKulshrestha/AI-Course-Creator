import os
import streamlit as st
from utils import content, link_to_image

st.title("AI Course Creator")

openai_key = st.text_input("Enter your OpenAI key", type='password')
serpapi_key = st.text_input("Enter your SerperAPI key", type='password')

os.environ['OPENAI_API_KEY'] = openai_key
os.environ['SERPER_API_KEY'] = serpapi_key


title = st.text_input("Enter the title of your course")

if st.button("Submit"):
    response = content(title)
    response = link_to_image(response)
    st.markdown(response)




