from typing import List
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.messages import HumanMessage, AIMessage
import httpx


def get_openai_llm(model_name: str, **kwargs):
    from langchain_openai.chat_models import ChatOpenAI
    return ChatOpenAI(model=model_name, **kwargs)

def get_ollama_llm(model_name: str, **kwargs):
    from langchain_ollama.llms import OllamaLLM
    return OllamaLLM(model=model_name, **kwargs)

def get_azure_llm(azure_deployment: str, api_version: str, **kwargs):
    from langchain_openai.chat_models import AzureChatOpenAI
    return AzureChatOpenAI(
            azure_deployment=azure_deployment,
            api_version=api_version,
            http_client= httpx.Client(verify = False),
            **kwargs
        )


def get_llm(provider: str, **kwargs):
    if provider == "openai":
        return get_openai_llm(**kwargs)
    elif provider == "ollama":
        return get_ollama_llm(**kwargs)
    elif provider == "azure":
        return get_azure_llm(**kwargs)
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")

# class OpenAILLMAdapter:
#     def __init__(self, model_name: str):
#         from langchain_openai.chat_models import ChatOpenAI
#         self.llm = ChatOpenAI(model=model_name)

# class OllamaLLMAdapter:
#     def __init__(self, model_name: str):
#         from langchain_ollama.llms import OllamaLLM
#         self.llm = OllamaLLM(model=model_name)

# class AzureOpenAILLMAdapter:
#     def __init__(self, azure_deployment: str, api_version: str):
#         from langchain_openai.chat_models import AzureChatOpenAI
#         self.llm = AzureChatOpenAI(
#             azure_deployment=azure_deployment,
#             api_version=api_version,
#             http_client= httpx.Client(verify = False)
#         )