from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Базовые схемы
class RepoEventBase(BaseModel):
    repo_name: str
    event_type: str
    actor_login: Optional[str] = None
    created_at: datetime

# Схема для создания (приходит из API или фоновой задачи)
class RepoEventCreate(RepoEventBase):
    payload: Optional[dict] = None
    raw_data: Optional[dict] = None

# Схема для ответа API (то, что мы отправляем клиенту)
class RepoEvent(RepoEventBase):
    id: str
    payload: Optional[dict] = None
    
    class Config:
        from_attributes = True  # Ранее orm_mode=True для Pydantic v2

# Схема для WebSocket-сообщения
class WSEventMessage(BaseModel):
    event_type: str = Field(..., description="Тип события: new_event, updated_event, deleted_event")
    data: RepoEvent