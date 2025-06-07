from typing import List
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.messages import HumanMessage, AIMessage
import httpx

class LLMInterface:
    def invoke(self, messages: List[HumanMessage | AIMessage]) -> str:
        raise NotImplementedError

class OpenAILLMAdapter(LLMInterface):
    def __init__(self, model_name: str):
        from langchain_openai.chat_models import ChatOpenAI
        self.llm = ChatOpenAI(model=model_name)

    def invoke(self, messages: List[HumanMessage | AIMessage]) -> str:
        response = self.llm.invoke(messages)
        return response.content

class OllamaLLMAdapter(LLMInterface):
    def __init__(self, model_name: str):
        from langchain_ollama.llms import OllamaLLM
        self.llm = OllamaLLM(model=model_name)

    def invoke(self, messages: List[HumanMessage | AIMessage]) -> str:
        response = self.llm.invoke(messages)
        return str(response)

class AzureOpenAILLMAdapter(LLMInterface):
    def __init__(self, azure_deployment: str, api_version: str):
        from langchain_openai.chat_models import AzureChatOpenAI
        self.llm = AzureChatOpenAI(
            azure_deployment=azure_deployment,
            api_version=api_version,
            http_client= httpx.Client(verify = False)
        )

    def invoke(self, messages: List[HumanMessage | AIMessage]) -> str:
        response  = self.llm.invoke(messages)
        return response.content
