import os

from dotenv import load_dotenv
from vector.embeddings import get_embeddings
from langchain.vectorstores import DeepLake

load_dotenv(".env")

my_activeloop_org_id = os.getenv("ACTIVE_LOOP_ORG_ID")
my_activeloop_dataset_name = "met_office_data"
dataset_path = f"hub://{my_activeloop_org_id}/{my_activeloop_dataset_name}"
db = DeepLake(dataset_path=dataset_path, embedding_function=get_embeddings())

def get_vector_store():
    return db