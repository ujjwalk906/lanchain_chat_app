from langchain_ollama.llms import OllamaLLM
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.messages import ChatMessage, AIMessage

def get_llm() -> BaseLanguageModel:
    return OllamaLLM(model="gemma3:4b")

def get_ai_response(messages:list[ChatMessage], llm:BaseLanguageModel) -> AIMessage:
    return llm.invoke(messages)
