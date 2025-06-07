from src.db.models import Message
from sqlalchemy.orm import Session
from typing import List

def get_messages(thread_id: str, db_session: Session) -> List[Message]:
    return db_session.query(Message).filter_by(thread_id=thread_id).order_by(Message.timestamp).all()

def messages_to_langchain(messages: List[Message]):
    from langchain_core.messages import HumanMessage, AIMessage
    return [
        HumanMessage(content=m.content) if m.role == "user" else AIMessage(content=m.content)
        for m in messages
    ]
def add_message(thread_id :str, role:str, content:str, db_session:Session):
    msg = Message(thread_id=thread_id, role=role, content=content)
    db_session.add(msg)
    db_session.commit()

def add_user_message(thread_id:str, message:str, db_session:Session):
    add_message(thread_id, 'user', message, db_session)

def add_ai_message(thread_id:str, message:str, db_session:Session):
    add_message(thread_id, 'ai', message, db_session)
