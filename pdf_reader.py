from io import StringIO
from io import BytesIO
from typing import List, Dict, Any
import re
from getpass import getpass
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.docstore.document import Document
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma, VectorStore
from langchain.chains.qa_with_sources import load_qa_with_sources_chain


def pdf_reader(file: BytesIO) -> List[str]:
    """Loads the pdf file and extract text from it. Performs preprocessing and text cleaning

    Input: file

    Output: List
    """
    loader = UnstructuredPDFLoader(file)
    docs = loader.load()
    output = []
    for page in docs:
        # Merge hyphenated words
        text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", page.page_content)
        # Fix newlines in the middle of sentences
        text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", text.strip())
        # Remove multiple newlines
        text = re.sub(r"\n\s*\n", "\n\n", text)

        output.append(text)

    return output


def text_to_docs(text: str) -> List[Document]:
    """Converts a string or list of strings to a list of Documents
    with metadata."""
    if isinstance(text, str):
        # Take a single string as one page.
        text = [text]
    page_docs = [Document(page_content=page) for page in text]

    # Add page numbers as metadata
    for i, doc in enumerate(page_docs):
        doc.metadata["page"] = i + 1

    # Split pages into chunks
    doc_chunks = []

    for doc in page_docs:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
            chunk_overlap=0,
        )
        chunks = text_splitter.split_text(doc.page_content)
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk, metadata={"page": doc.metadata["page"], "chunk": i}
            )
            # Add sources a metadata
            doc.metadata["source"] = f"{doc.metadata['page']}-{doc.metadata['chunk']}"
            doc_chunks.append(doc)
    return doc_chunks


def embed_docs(docs: List[Document]) -> VectorStore:
    """Embeds a list of Documents and returns a Chroma index"""
    # Embed the chunks
    embeddings = OpenAIEmbeddings()
    persist_directory = 'vector_db'
    index = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
    # Saving the Vector store
    index.persist()
    return index


def search_docs(index: VectorStore, topic: str) -> List[Document]:
    """Searches a Chroma Vector index for similar chunks to the query
    and returns a list of Documents."""
    # Search for similar chunks. k determines the number of nearest neighbours
    docs = index.similarity_search(topic, k=2)
    return docs


def get_answer(docs: List[Document], topic: str) -> Dict[str, Any]:
    """Gets an answer to a question from a list of Documents."""
    with open('content_template.txt', 'r') as f:
        template = f.read()
    prompt = PromptTemplate(
        input_variables=['summaries', 'topic'],
        template=template,
    )
    chain = load_qa_with_sources_chain(OpenAI(temperature=0), chain_type="stuff", prompt=prompt)
    # retrievalQA = RetrievalQA.from_llm(llm=OpenAI(), retriever=index)

    answer = chain(
        {"input_documents": docs, "topic": topic}, return_only_outputs=True
    )
    return answer


# Not being used currently
def get_sources(answer: Dict[str, Any], docs: List[Document]) -> List[Document]:
    """Gets the source documents for an answer."""

    # Get sources for the answer
    source_keys = [s for s in answer["output_text"].split("SOURCES: ")[-1].split(", ")]

    source_docs = []
    for doc in docs:
        if doc.metadata["source"] in source_keys:
            source_docs.append(doc)

    return source_docs
