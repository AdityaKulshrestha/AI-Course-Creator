import streamlit as st
from utils import openai_env, serpapi_env, content, image_request, images_caption

st.title("AI Course Creator")

openai_key = st.text_input("Enter your OpenAI key", value='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', type = 'password')
serpapi_key = st.text_input("Enter your SerperAPI key",value='db6cfb60742df4fc29ad54a8c56434346cce3820', type='password')

openai_env(openai_key)
serpapi_env(serpapi_key)


title = st.text_input("Enter the title of your course")

if st.button("Submit"):
    response = content(title)
    st.text(response)
    img_url = content(title)
    st.image(img_url)



