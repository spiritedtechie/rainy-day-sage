import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from vector.vector_store import get_vector_store

db = get_vector_store()

document_loader = PyPDFLoader(file_path="data/met_office/datapoint_api_reference.pdf")
document = document_loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(document)
db.add_documents(docs)
print("Storing document in vector store")
