from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

response_schemas = [
    ResponseSchema(name="summary", description="summary of the weather"),
    ResponseSchema(name="full", description="full breakdown of the weather"),
    ResponseSchema(
        name="status",
        description="status of the weather - can be one of: Poor, Fair, Average, Good or Very Good",
    ),
    ResponseSchema(
        name="inspiring-message",
        description="uplifting message about the weather",
    ),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

template = """
On the following lines is a CSV representation of the weather forecast for the next few days. 
The first row contains the column names. 
The datetime column is in format '%Y-%m-%d %H:%M:%S'. Each row represents a three-hour forecast from the row's datetime.
Use only this data for the summary.
Match the supplied datetime to that in the data.
-----
{csv}
-----
Use the following codes mappings to map any codes to meaningful words.
-----
{code_mappings}
-----
{format_instructions}
"""

human_template = """
The current datetime is: {datetime}
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
    input_variables=["code_mappings", "csv", "datetime"],
)


def get_prompt():
    return output_parser, chat_prompt
