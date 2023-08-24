# In this codebase, I have a function that transform the Met Office JSON data to CSV
# Here, I played around to see if an LLM could do this transform directly without needing code.


import json
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate
from log_config import get_logger

load_dotenv(".env")

log = get_logger()

open_ai_api_key = os.getenv("OPENAI_API_KEY")

template = """
Each rep has a '$' field which represent the "minutes from midnight" from the period date.
For example, if the period date is 2023-07-10, and the $ value is 540, this represents 2023-07-10 09:00:00.
---------
{json}
---------
Include the CSV on a single line.
Include the header row with field names and units.
Include the calculated DateTime for each row.
"""

question = """
Convert the data to CSV format.
"""

chat_prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(template),
    ],
    input_variables=["json"],
)


# Create the LLM reference
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo", temperature=0, openai_api_key=open_ai_api_key
)

# Create the chains
chain = LLMChain(llm=llm, prompt=chat_prompt, output_key="result", verbose=True)


# Read the sample JSON
with open("data/met_office/sample_forecast_data_slim.json") as file:
    file_contents = file.read()
    json = json.loads(file_contents)

# Execute LLM chain
with get_openai_callback() as cb:
    response = chain(
        {
            "json": json,
        },
        return_only_outputs=True,
    )
    log.debug(response)

    print(response["result"])

    log.debug(cb)
