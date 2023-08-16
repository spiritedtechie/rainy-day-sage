import os

import requests
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

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
template = """
-----
On the following lines is a CSV representation of the weather for the next few days. The first line contains the column names.
{csv}
-----
"""
system_message_prompt = SystemMessagePromptTemplate.from_template(template)

human_template = """
Can you summarise the weather for today? If the weather is bad, also give an wise and uplifting message to lighten the mood about the weather.
"""
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)

# Create the LLM reference
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=open_ai_api_key,
)

# Ask the LLM the question
with get_openai_callback() as cb:
    chain = LLMChain(
        llm=llm,
        prompt=chat_prompt,
    )
    response = chain.run(csv=data_as_csv)

    print(response)
    print(cb)
