from pydantic import BaseModel, Field, Validator
from typing import Type
from langchain.output_parsers import PydanticOutputParser
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.output_parsers.enum import EnumOutputParser
from langchain.output_parsers import PandasDataFrameOutputParser
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.output_parsers import XMLOutputParser
from langchain.output_parsers import YamlOutputParser
from components.outputs.parsers.validator import OutputValidator

def create_pydantic_model(name:str, fields:dict, validations:dict)->Type[BaseModel]:
    """
    Create a Pydantic model dynamically.

    :param name: Name of the Pydantic model.
    :param fields: Dictionary where keys are field names and values are tuples of (type, Field).
    :param validations: Dictionary where keys are field names and values are validation functions.
    :return: Pydantic model class.
    """
    model_dict = {
        '__anotations__':{field_name:field_type for field_name, (field_type, _) in fields.items()},
        **{field_name: field for field_name, (_, field) in fields.items()}
    }

    for field_name, validation in validations.items():
        model_dict[f'validate_{field_name}'] = Validator(field_name, allow_reuse=True)(validation)

    return type(name, (BaseModel,), model_dict)


class Parser():
    def CSVParser():
        parser= CommaSeparatedListOutputParser()
        return parser
    
    def ENUMParser(enum):
        parser = EnumOutputParser(enum)
        return parser
    
    def PandasDataframeParser(dataframe):
        parser = PandasDataFrameOutputParser(dataframe=dataframe)
        return parser
    
    def StructuredParser(response_list: list[tuple[str, str]]):
        response_schemas = [
            ResponseSchema(name=name, description=description)
            for name, description in response_list
        ]
        parser = StructuredOutputParser(response_schemas=response_schemas)
        return parser
    
    def XMLParser():
        parser = XMLOutputParser()
        return parser
    
    def PydanticParser(name, fields, validations):
        pydantic_model = create_pydantic_model(name= name, fields=fields, validations=validations)
        return pydantic_model

#***************EXAMPLE USAGE***************
# fields = {
#     'setup': (str, Field(description="question to set up a joke")),
#     'punchline': (str, Field(description="answer to resolve the joke"))
# }

# validations = {
#     'setup': vl.ends_with_question_mark
# }


