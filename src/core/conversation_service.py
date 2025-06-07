# conversations_service.py

from typing import List, Optional
from sqlalchemy.orm import Session
from src.db.models import Conversation, get_session, get_engine
import uuid
import datetime

def create_conversation(name: str, db_session: Session) -> Conversation:
    """
    Creates a new conversation with a unique thread_id and returns it.
    """
    conversation = Conversation(
        thread_id=str(uuid.uuid4()),
        name=name,
        created_at=datetime.datetime.utcnow()
    )
    db_session.add(conversation)
    db_session.commit()
    db_session.refresh(conversation)
    return conversation

def list_conversations(db_session: Session) -> List[Conversation]:
    """
    Returns all conversations in the database, newest first.
    """
    return db_session.query(Conversation).order_by(Conversation.created_at.desc()).all()

def get_conversation_by_id(db_session: Session, thread_id: str) -> Optional[Conversation]:
    """
    Returns a conversation by its thread_id.
    """
    return db_session.query(Conversation).filter_by(thread_id=thread_id).first()

def get_conversation_by_name(db_session: Session, name: str) -> Optional[Conversation]:
    """
    Returns a conversation by its name.
    """
    return db_session.query(Conversation).filter_by(name=name).first()

def delete_conversation(db_session: Session, thread_id: str) -> bool:
    """
    Deletes a conversation and all its messages (cascading delete recommended).
    """
    conversation = get_conversation_by_id(db_session, thread_id)
    if conversation:
        db_session.delete(conversation)
        db_session.commit()
        return True
    return False

def rename_conversation(db_session: Session, thread_id: str, new_name: str) -> None:
    """
    Renames a conversation.
    """
    conversation = get_conversation_by_id(db_session, thread_id)
    if conversation:
        conversation.name = new_name
        db_session.commit()

# Example usage for testing/debugging:
if __name__ == "__main__":
    engine = get_engine()
    session = get_session(engine)
    for c in list_conversations(session):
        print(f"{c.thread_id}: {c.name} ({c.created_at})")
