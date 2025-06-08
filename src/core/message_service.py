from src.db.models import Message
from sqlalchemy.orm import Session
from typing import List
from src.api.schemas.messages import MessageOut

# 1. DB Layer: Query for all messages in a conversation
def get_messages(thread_id: str, db_session: Session) -> List[Message]:
    return (
        db_session
        .query(Message)
        .filter_by(thread_id=thread_id)
        .order_by(Message.timestamp)
        .all()
    )

# 2. Conversion: ORM Messages -> LangChain Message objects
def messages_to_langchain(messages: List[Message]):
    from langchain_core.messages import HumanMessage, AIMessage
    return [
        HumanMessage(content=m.content) if m.role == "user" else AIMessage(content=m.content)
        for m in messages
    ]

# 3. Conversion: ORM Message -> API Schema
def message_to_schema(m: Message) -> MessageOut:
    return MessageOut(
        id=m.id,
        conversation_id=m.thread_id,
        role=m.role,
        content=m.content,
        timestamp=m.timestamp,
    )

# 4. Add message to DB and return the ORM Message object
def add_message(thread_id: str, role: str, content: str, db_session: Session) -> Message:
    msg = Message(thread_id=thread_id, role=role, content=content)
    db_session.add(msg)
    db_session.commit()
    db_session.refresh(msg)
    return msg

def add_user_message(thread_id: str, message: str, db_session: Session) -> Message:
    return add_message(thread_id, 'user', message, db_session)

def add_ai_message(thread_id: str, message: str, db_session: Session) -> Message:
    return add_message(thread_id, 'ai', message, db_session)
