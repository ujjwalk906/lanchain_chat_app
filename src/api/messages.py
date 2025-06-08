from fastapi import APIRouter, HTTPException, Depends
from typing import List
from src.api.schemas.messages import MessageCreate, MessageOut
from src.core.message_service import (
    get_messages,
    add_user_message,
    add_ai_message,
    messages_to_langchain,
    message_to_schema
)
from src.core.conversation_service import get_conversation_by_id
from src.core.llm_adapters import get_llm
from src.core.chat_engine import get_ai_response

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

@router.post("/conversations/{conversation_id}/messages", response_model=List[MessageOut])
def api_send_message(conversation_id: str, message: MessageCreate, db_session=Depends(get_session)):
    # 1. Validate conversation exists
    conversation = get_conversation_by_id(db_session, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # 2. Add user message to DB
    user_msg = add_user_message(conversation_id, message.content, db_session)

    # 3. Get full conversation history from DB (can window if needed)
    db_history = get_messages(conversation_id, db_session)

    # 4. Convert DB messages to LangChain history
    lc_history = messages_to_langchain(db_history)

    # 5. Get the correct LLM instance
    llm = get_llm(
        conversation.provider,
        model_name=conversation.model_name,
        # Add other needed config (api_key, endpoint) if stored
    )

    # 6. Get AI response using the chat engine's unified function
    ai_content = get_ai_response(lc_history, llm)

    # 7. Add AI reply to DB
    ai_msg = add_ai_message(conversation_id, ai_content, db_session)

    # 8. Return both messages as API response (user then AI)
    return [message_to_schema(user_msg), message_to_schema(ai_msg)]