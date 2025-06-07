from langchain_ollama.llms import OllamaLLM
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.messages import HumanMessage, AIMessage
from src.core.llm_adapters import LLMInterface,OpenAILLMAdapter,OllamaLLMAdapter,AzureOpenAILLMAdapter

def get_llm(provider: str, **kwargs) -> LLMInterface:
    if provider == "openai":
        return OpenAILLMAdapter(kwargs["model_name"])
    elif provider == "ollama":
        return OllamaLLMAdapter(kwargs["model_name"])
    elif provider == "azure":
        return AzureOpenAILLMAdapter(
            kwargs["azure_deployment"],
            kwargs["api_version"]
        )
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")

def get_ai_response(messages:list[HumanMessage | AIMessage], llm:BaseLanguageModel) -> AIMessage:
    return llm.invoke(messages)

if __name__ == "__main__":
    llm = get_llm("ollama",model_name = "llama3.2:1b-instruct-q8_0")
    print(llm.invoke("hi"))