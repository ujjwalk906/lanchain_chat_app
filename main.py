# cli.py
import uuid
from src.db.models import get_engine, get_session, initialize_database, Conversation
from src.core.message_service import get_messages, add_user_message, add_ai_message
from src.core.llm_adapters import get_llm

def create_conversation(db_session, name):
    thread_id = str(uuid.uuid4())
    conversation = Conversation(thread_id=thread_id, name=name)
    db_session.add(conversation)
    db_session.commit()
    return thread_id

def cli_chat():
    # --- Setup ---
    # engine = get_engine()
    # initialize_database(engine)
    # db_session = get_session(engine)
    # print(get_messages("1665c514-f86a-410c-9f08-7182b87daf82", db_session=db_session))
    # # api_key = input("Enter your OpenAI API key: ").strip()

    # from langchain_core.messages import HumanMessage
    llm = get_llm('ollama',model_name = "llama3.2:1b-instruct-q8_0")
    print(llm.invoke("hi"))

    # # --- New conversation ---
    # conversation_name = input("Enter a name for your conversation: ")
    # thread_id = create_conversation(db_session, conversation_name)
    # print(f"Starting conversation '{conversation_name}' (ID: {thread_id})")

    # while True:
    #     user_input = input("You: ")
    #     if user_input.lower() == "exit":
    #         break

    #     add_user_message(thread_id, user_input, db_session)
    #     messages = get_messages(thread_id, db_session)
    #     response = get_ai_response(messages, llm)
    #     add_ai_message(thread_id, response, db_session)
    #     print(f"AI: {response}")

    #     # for openai models use this
    #     # add_ai_message(thread_id, response.content, db_session)
    #     # print(f"AI: {response.content}")

if __name__ == "__main__":
    cli_chat()
