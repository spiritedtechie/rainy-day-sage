import os

import requests
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)

from convert_to_csv import convert_to_csv
from transform_forecast_data import transform_data

load_dotenv(".env")

open_ai_api_key = os.getenv("OPENAI_API_KEY")
met_office_api_key = os.getenv("MET_OFFICE_KEY")

# Get today's weather forecast from the API
met_office_data = requests.get(
    "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/351033?res=3hourly",
    params={"res": "3hourly", "key": met_office_api_key},
)

# Convert it to a compact CSV
object_list, object_keys = transform_data(met_office_data.json())
data_as_csv = convert_to_csv(object_list, object_keys)

# Build the prompt
response_schemas = [
    ResponseSchema(name="summary", description="A summary of the weather in 100 words"),
    ResponseSchema(
        name="status",
        description="A prediction of if the weather. Can be one of: Poor, Fair, Average, Good or Very Good",
    ),
    ResponseSchema(
        name="inspiring-message",
        description="An optional uplifting message about the weather",
    ),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()


template = """
On the following lines is a CSV representation of the weather for the next few days. The first line contains the column names. 
The datetime column is in format '%Y-%m-%d %H:%M:%S'.
-----
{csv}
-----
{format_instructions}
"""

human_template = """
Summarise the weather for the next few hours of today. Based on the predicted status, 
give an appropriate wise and uplifting message. For example if the weather is Poor,
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
    model_name="gpt-3.5-turbo", temperature=0.5, openai_api_key=open_ai_api_key
)

chain = LLMChain(llm=llm, prompt=chat_prompt, verbose=True)

# Ask the LLM the question
with get_openai_callback() as cb:
    response = chain.run(csv=data_as_csv)
    print(response)
    print(cb)
