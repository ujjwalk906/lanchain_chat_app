from pydantic import BaseModel
from datetime import datetime


class ConversationCreate(BaseModel):
    name: str
    provider: str
    model_name: str

class ConversationOut(BaseModel):
    id: str
    name: str
    provider: str
    model_name: str
    created_at: datetime
    last_message: str | None = None
    last_updated: datetime | None = None


class ConversationUpdate(BaseModel):
    name: str

class DeleteResponse(BaseModel):
    success: bool
    detail: str | None = None