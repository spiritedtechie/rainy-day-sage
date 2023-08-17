# To extract more concise and formatted code mappings from API document
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

response_schemas = [
    ResponseSchema(
        name="weather type",
        type="json",
        description="significant weather code mappings",
    ),
    ResponseSchema(
        name="visibility",
        type="json",
        description="visibility code mappings",
    ),
    ResponseSchema(name="uv", type="json", description="UV index mappings"),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

template = """
Meaningful labels should be extracted from the following, extracting 
codes for significant weather, UV and visibility:
---------
{api_documents}
---------
{format_instructions}
"""

human_template = """
Extract meaningful labels against the codes.
"""

chat_prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(template),
        HumanMessagePromptTemplate.from_template(human_template),
    ],
    partial_variables={"format_instructions": format_instructions},
    input_variables=["api_documents"],
)


def get_prompt():
    return chat_prompt
