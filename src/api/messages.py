from fastapi import APIRouter, HTTPException, Depends
from typing import List
from src.api.schemas.messages import MessageCreate, MessageOut
from src.core.message_service import (
    get_messages,
    add_user_message,
    add_ai_message,
    messages_to_langchain
)
from src.core.conversation_service import get_conversation_by_id
from src.db.models import get_session
router = APIRouter()

@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageOut])
def api_get_messages(conversation_id: str, db_session=Depends(get_session)):
    db_messages = get_messages(conversation_id, db_session)
    return [MessageOut(
        id=m.id,
        conversation_id=m.thread_id,
        role=m.role,
        content=m.content,
        timestamp=m.timestamp,
    ) for m in db_messages]
