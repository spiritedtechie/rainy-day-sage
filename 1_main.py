import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import CacheBackedEmbeddings, OpenAIEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.storage import LocalFileStore
from langchain.vectorstores import DeepLake

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

# Build the prompt
response_schemas = [
    ResponseSchema(name="summary", description="A summary of the weather"),
    ResponseSchema(name="full", description="A full breakdown of the weather"),
    ResponseSchema(
        name="status",
        description="A status of the weather. Can be one of: Poor, Fair, Average, Good or Very Good",
    ),
    ResponseSchema(
        name="inspiring-message",
        description="An uplifting message about the weather",
    ),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

template = """
On the following lines is a CSV representation of the weather forecast for the next few days. 
The first row contains the column names. 
The datetime column is in format '%Y-%m-%d %H:%M:%S'. Each row represents a three-hour forecast from the row's datetime.
The Weather Type is also known as Significant Weather.
Use only this data for the summary and only the relevant datetimes.
-----
{csv}
-----
Use the following context to map any codes to words.
-----
{context}
-----
{format_instructions}
"""

human_template = """
The current date & time is: {datetime}
Summarise the weather for the next three hours as follows:
1. Summarise like you are a weatherman, in no more than 150 words.
2. Create a more detailed breakdown in no more than 200 words.
3. Include the predicted status.
4. Give an inspiring message based on the predicted status. For example if the weather is deemed 'Poor',
give an uplifting message to lighten the mood.
"""

chat_prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(template),
        HumanMessagePromptTemplate.from_template(human_template),
    ],
    partial_variables={"format_instructions": format_instructions},
)

# Create the LLM reference
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo", temperature=0.2, openai_api_key=open_ai_api_key
)

# Create the chain
chain = load_qa_chain(llm=llm, chain_type="stuff", prompt=chat_prompt, verbose=True)

# Ask the question
with get_openai_callback() as cb:
    response = chain(
        {
            "input_documents": docs,
            "csv": data_as_csv,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
        return_only_outputs=True,
    )
    print(response)
    print(cb)
