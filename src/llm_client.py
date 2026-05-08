import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_llm_client():
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")

    if not api_key:
        raise ValueError("LLM_API_KEY is not set in your .env file")

    return OpenAI(api_key=api_key, base_url=base_url)

def get_model():
    model = os.getenv("LLM_MODEL")
    if not model:
        raise ValueError("LLM_MODEL is not set in your .env file")
    return model