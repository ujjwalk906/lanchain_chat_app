# cli.py
import uuid
from db import get_engine, get_session, initialize_database, Conversation
from history import get_messages, add_user_message, add_ai_message
from chat_engine import get_llm, get_ai_response

def create_conversation(db_session, name):
    thread_id = str(uuid.uuid4())
    conversation = Conversation(thread_id=thread_id, name=name)
    db_session.add(conversation)
    db_session.commit()
    return thread_id

def cli_chat():
    # --- Setup ---
    engine = get_engine()
    initialize_database(engine)
    db_session = get_session(engine)
    api_key = input("Enter your OpenAI API key: ").strip()
    llm = get_llm()

    # --- New conversation ---
    conversation_name = input("Enter a name for your conversation: ")
    thread_id = create_conversation(db_session, conversation_name)
    print(f"Starting conversation '{conversation_name}' (ID: {thread_id})")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        add_user_message(thread_id, user_input, db_session)
        messages = get_messages(thread_id, db_session)
        response = get_ai_response(messages, llm)
        add_ai_message(thread_id, response.content, db_session)
        print(f"AI: {response.content}")

if __name__ == "__main__":
    cli_chat()
