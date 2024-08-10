import os
from dotenv import load_dotenv
from openai import OpenAI, AzureOpenAI
from components.constants import LLMSource

load_dotenv()
def get_llm(llm_source, llm_model):
    
    if llm_source is LLMSource.AZURE:
        return AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),  
    api_version="2024-02-01",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    if llm_source is LLMSource.OPENAI:
        return OpenAI(openai_api_key=os.getenv("OPENAI_KEY"))