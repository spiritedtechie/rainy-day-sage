import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from langchain.chains import LLMChain, SequentialChain, TransformChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import CacheBackedEmbeddings, OpenAIEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.storage import LocalFileStore
from langchain.vectorstores import DeepLake

import prompts.code_mapping_extract
import prompts.weather_summary
from convert_to_csv import convert_to_csv
from transform_forecast_data import transform_data

load_dotenv(".env")

open_ai_api_key = os.getenv("OPENAI_API_KEY")
met_office_api_key = os.getenv("MET_OFFICE_KEY")

# Get today's weather forecast from the API in JSON
met_office_data = requests.get(
    "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/351033?res=3hourly",
    params={"res": "3hourly", "key": met_office_api_key},
)

# Convert it to a more meaningful, compact CSV to reduce tokens
object_list, object_keys = transform_data(met_office_data.json())
data_as_csv = convert_to_csv(object_list, object_keys)


# Get the relevant sections of the API reference i.e. codes and their meaning
# Using a vector search
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
fs = LocalFileStore("./cache/")
cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    embeddings, fs, namespace=embeddings.model
)
activeloop_org_id = os.getenv("ACTIVE_LOOP_ORG_ID")
activeloop_dataset_name = "met_office_data"
dataset_path = f"hub://{activeloop_org_id}/{activeloop_dataset_name}"
db = DeepLake(dataset_path=dataset_path, embedding_function=cached_embedder)
retriever = db.as_retriever(search_kwargs={"k": 5})

docs = retriever.get_relevant_documents("Codes for weather type, visibility and UV")


# Prompts
code_extract_prompt = prompts.code_mapping_extract.get_prompt()
weather_summary_prompt = prompts.weather_summary.get_prompt()

# Create the LLM reference
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo", temperature=0, openai_api_key=open_ai_api_key
)

# Create the chains
code_extract_chain = LLMChain(
    llm=llm,
    prompt=code_extract_prompt,
    output_key="code_mappings",
    verbose=True,
)

summary_chain = LLMChain(
    llm=llm, prompt=weather_summary_prompt, output_key="result", verbose=True
)

overall_chain = SequentialChain(
    chains=[code_extract_chain, summary_chain],
    input_variables=["api_documents", "csv", "datetime"],
    output_variables=["result"],
    verbose=True,
)

# Ask the question
docs = [{"doc": doc.page_content} for doc in docs]

with get_openai_callback() as cb:
    response = overall_chain(
        {
            "api_documents": docs,
            "csv": data_as_csv,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
        return_only_outputs=True,
    )
    print(response)
    print(cb)
