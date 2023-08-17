import os

from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import CacheBackedEmbeddings, OpenAIEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.storage import LocalFileStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import DeepLake

load_dotenv(".env")

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
fs = LocalFileStore("./cache/")
cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    embeddings, fs, namespace=embeddings.model
)

my_activeloop_org_id = os.getenv("ACTIVE_LOOP_ORG_ID")
my_activeloop_dataset_name = "met_office_data"
dataset_path = f"hub://{my_activeloop_org_id}/{my_activeloop_dataset_name}"
db = DeepLake(dataset_path=dataset_path, embedding_function=cached_embedder)

document_loader = PyPDFLoader(file_path="data/met_office/datapoint_api_reference.pdf")
document = document_loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(document)
db.add_documents(docs)
print("Storing document in vector store")
