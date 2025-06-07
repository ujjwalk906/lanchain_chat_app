from langchain_ollama.llms import OllamaLLM
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.messages import HumanMessage, AIMessage

def get_llm(model_name:str) -> BaseLanguageModel:
    return OllamaLLM(model=model_name)

def get_ai_response(messages:list[HumanMessage | AIMessage], llm:BaseLanguageModel) -> AIMessage:
    return llm.invoke(messages)

if __name__ == "__main__":
    llm = get_llm("llama3.2:1b-instruct-q8_0")
    print(llm.invoke("hi"))