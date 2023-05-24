from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.callbacks import get_openai_callback
import re
import os
import streamlit as st
from utils import content, link_to_image


def content(title):
    with open('content_template.txt', 'r') as f:
        template = f.read()
    prompt = PromptTemplate(
        input_variables=["topic"],
        template=template,
    )
    with get_openai_callback() as cb:
        chain = LLMChain(llm=ChatOpenAI(temperature=0.9), prompt=prompt)
        return chain.run(title), cb


def image_request(caption):
    search = GoogleSerperAPIWrapper(type="images")
    results = search.results(caption.group()[1:-1])
    return f"![{caption.group()[1:-1]}]({results['images'][0]['imageUrl']})"
    # return f"<p> \n <img src='{results['images'][0]['imageUrl']}' width=400 height=400 /> </p>"


# Replace image description with image link
def link_to_image(response):
    response = re.sub(r'\<(.*?)\>', lambda match: image_request(match), response)
    return response


st.title("AI Course Creator")

openai_key = st.text_input("Enter your OpenAI key", type='password')
serpapi_key = st.text_input("Enter your SerperAPI key", type='password')

os.environ['OPENAI_API_KEY'] = openai_key
os.environ['SERPER_API_KEY'] = serpapi_key


title = st.text_input("Enter the title of your course")

if st.button("Submit"):
    response, tokens = content(title)
    # st.text("Tokens used: {}".format(tokens))
    # print(response)
    response = link_to_image(response)
    # st.text(response)
    st.markdown(response)