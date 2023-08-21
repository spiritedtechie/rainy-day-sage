import os

from dotenv import load_dotenv
from vector.embeddings import get_embeddings
from langchain.vectorstores import DeepLake

load_dotenv(".env")

my_activeloop_org_id = os.getenv("ACTIVE_LOOP_ORG_ID")

def get_vector_store(dataset_name, read_only=False):
    dataset_path = f"hub://{my_activeloop_org_id}/{dataset_name}"
    return DeepLake(dataset_path=dataset_path, read_only=read_only, embedding_function=get_embeddings())