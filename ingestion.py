
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

load_dotenv()
import google.generativeai as genai



# embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


# Print the names of the models
# models = genai.list_models()
# print("Available Google LLM Models:")
# for model in models:
#     print(model.name)

UNIVERSITY_URLS = [
    "https://www.uchicago.edu/",
    "https://www.washington.edu/",
    "https://www.stanford.edu/",
    "https://und.edu/"
]

def scrape_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for script in soup(['script', 'style']):
        script.decompose()
    text = soup.get_text(separator=' ', strip=True)
    return text, url

def ingest_docs():
    raw_documents = []
    for url in UNIVERSITY_URLS:
        try:
            text, source_url = scrape_url(url)
            # print(text,'=====ingest_docs======')
            doc = Document(page_content=text, metadata={"source": source_url})
            raw_documents.append(doc)
        except Exception as e:
            print(f"Failed to load {url}: {e}")

    print(f"Loaded {len(raw_documents)} documents")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    documents = text_splitter.split_documents(raw_documents)

    print(f"Going to add {len(documents)} chunks to FAISS")
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(r"D:\University_Bot\University_Bot_faiss\faiss_index\index.faiss")
    print("**** FAISS vectorstore saved locally ****")

if __name__ == "__main__":
    ingest_docs()
