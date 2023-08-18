import os

from dotenv import load_dotenv
from langchain.embeddings import CacheBackedEmbeddings, OpenAIEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.storage import LocalFileStore

load_dotenv(".env")

open_ai_api_key = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002", openai_api_key=open_ai_api_key
)
fs = LocalFileStore("./cache/")
cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    embeddings, fs, namespace=embeddings.model
)


def get_embeddings():
    return cached_embedder
