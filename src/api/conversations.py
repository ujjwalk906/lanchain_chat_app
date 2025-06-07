from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from src.api.schemas.conversations import (
    ConversationCreate, ConversationOut, ConversationUpdate, DeleteResponse
)
from src.core.conversation_service import (
    list_conversations, get_conversation_by_id,
    create_conversation, delete_conversation, rename_conversation
)
from src.db.models import get_session

router = APIRouter()

@router.get("/conversations", response_model=List[ConversationOut])
def api_list_conversations(db_session=Depends(get_session)):
    conversations = list_conversations(db_session)
    return [
        ConversationOut(
            id=c.thread_id,
            name=c.name,
            provider=c.provider,
            model_name=c.model_name,
            created_at=c.created_at,
        )
        for c in conversations
    ]

@router.post("/conversations", response_model=ConversationOut, status_code=status.HTTP_201_CREATED)
def api_create_conversation(conv: ConversationCreate, db_session=Depends(get_session)):
    c = create_conversation(conv.name, conv.provider, conv.model_name, db_session)
    return ConversationOut(
        id=c.thread_id,
        name=c.name,
        provider=c.provider,
        model_name=c.model_name,
        created_at=c.created_at
    )

@router.patch("/conversations/{conversation_id}", response_model=ConversationOut)
def api_rename_conversation(conversation_id: str, update: ConversationUpdate, db_session=Depends(get_session)):
    c = rename_conversation(db_session, conversation_id, update.name)
    if not c:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return ConversationOut(
            id=c.thread_id,
            name=c.name,
            provider=c.provider,
            model_name=c.model_name,
            created_at=c.created_at,
        )

@router.delete("/conversations/{conversation_id}", response_model=DeleteResponse)
def api_delete_conversation(conversation_id: str, db_session=Depends(get_session)):
    deleted = delete_conversation(db_session, conversation_id)
    return DeleteResponse(success=deleted, detail="Deleted" if deleted else "Not found")
