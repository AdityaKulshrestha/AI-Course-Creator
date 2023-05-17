import streamlit as st
from utils import openai_env, serpapi_env, content, image_request, images_caption

st.title("AI Course Creator")

openai_key = st.text_input("Enter your OpenAI key", type = 'password')
serpapi_key = st.text_input("Enter your SerperAPI key", type='password')

openai_env(openai_key)
serpapi_env(serpapi_key)


title = st.text_input("Enter the title of your course")

if st.button("Submit"):
    response = content(title)
    st.text(response)
    img_url = content(title)
    st.image(img_url)



