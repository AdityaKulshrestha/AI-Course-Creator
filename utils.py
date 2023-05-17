import os
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import GoogleSerperAPIWrapper


def openai_env(key):
    os.environ['OPENAI_API_KEY'] = key


def serpapi_env(key):
    os.environ['SERPER_API_KEY'] = key


def content(title):
    with open('content_template.txt','r') as f:
        template = f.read()
    prompt = PromptTemplate(
        input_variables=["product"],
        template=template,
    )
    chain = LLMChain(llm=ChatOpenAI(), prompt=prompt)
    return chain.run(title)


def images_caption(title):
    with open('images_template.txt','r') as f:
        template_images = f.read()
    prompt_images = PromptTemplate(
        input_variables=["topic"],
        template=template_images,
    )
    chain = LLMChain(llm=ChatOpenAI(), prompt=prompt_images)
    return chain.run(title)


def image_request(caption):
    search = GoogleSerperAPIWrapper(type="images")
    results = search.results(caption)
    return results['images'][0]['imageUrl']






