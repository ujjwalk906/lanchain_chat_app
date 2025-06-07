# history.py
from langchain_core.messages import HumanMessage, AIMessage
from src.db.models import Message

def get_messages(thread_id, db_session):
    records = db_session.query(Message).filter_by(thread_id=thread_id).order_by(Message.timestamp).all()
    return [
        HumanMessage(content=record.content) if record.role == 'user' else AIMessage(content=record.content)
        for record in records
    ]

def add_message(thread_id, role, content, db_session):
    msg = Message(thread_id=thread_id, role=role, content=content)
    db_session.add(msg)
    db_session.commit()

def add_user_message(thread_id, message, db_session):
    add_message(thread_id, 'user', message, db_session)

def add_ai_message(thread_id, message, db_session):
    add_message(thread_id, 'ai', message, db_session)
