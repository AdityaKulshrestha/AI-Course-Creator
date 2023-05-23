from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.utilities import GoogleSerperAPIWrapper
import re


def content(title):
    with open('content_template.txt', 'r') as f:
        template = f.read()
    prompt = PromptTemplate(
        input_variables=["topic"],
        template=template,
    )
    chain = LLMChain(llm=ChatOpenAI(), prompt=prompt)
    return chain.run(title)


def image_request(caption):
    search = GoogleSerperAPIWrapper(type="images")
    results = search.results(caption.group()[1:-1])
    return f"![{caption.group()[1:-1]}]({results['images'][0]['imageUrl']})"


# Replace image description with image link
def link_to_image(response):
    response = re.sub(r'\<(.*?)\>', lambda match: image_request(match), response)
    return response
