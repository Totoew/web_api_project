from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.api.dependencies import get_db_session
from app.schemas.repo_event import RepoEvent, RepoEventCreate
from app.services.event_service import EventService
from app.websocket.ws_manager import ws_manager
from app.nats.publisher import publish_event_created

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/events", tags=["events"])

@router.get("/", response_model=List[RepoEvent])
async def read_events(
    skip: int = Query(0, ge=0, description="Количество пропущенных записей"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    db: AsyncSession = Depends(get_db_session),
):
    """Получить список событий с пагинацией"""
    logger.info(f"GET /events called with skip={skip}, limit={limit}")
    events = await EventService.get_all_events(db, skip=skip, limit=limit)
    logger.info(f"Returning {len(events)} events")
    return events

@router.get("/{event_id}", response_model=RepoEvent)
async def read_event(
    event_id: str,
    db: AsyncSession = Depends(get_db_session),
):
    """Получить конкретное событие по ID"""
    logger.info(f"GET /events/{event_id} called")
    event = await EventService.get_event(db, event_id)
    if event is None:
        logger.warning(f"Event {event_id} not found")
        raise HTTPException(status_code=404, detail="Event not found")
    logger.info(f"Returning event {event_id}")
    return event

@router.post("/", response_model=RepoEvent, status_code=201)
async def create_event(
    event_data: RepoEventCreate,
    db: AsyncSession = Depends(get_db_session),
):
    """Создать новое событие (вручную через API)"""
    logger.info(f"POST /events called with data: {event_data.model_dump()}")
    # Создаем событие в БД
    event = await EventService.create_event(db, event_data)
    
    # Отправляем уведомление через WebSocket
    await ws_manager.broadcast_event("new_event", event)
    
    # Публикуем событие в NATS
    await publish_event_created(event)
    
    logger.info(f"Event created with ID: {event.id}")
    return event

@router.delete("/{event_id}", status_code=204)
async def delete_event(
    event_id: str,
    db: AsyncSession = Depends(get_db_session),
):
    """Удалить событие по ID"""
    logger.info(f"DELETE /events/{event_id} called")
    # Сначала получаем событие, чтобы отправить его в WS
    event = await EventService.get_event(db, event_id)
    if event is None:
        logger.warning(f"Event {event_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Удаляем событие
    success = await EventService.delete_event(db, event_id)
    if not success:
        logger.error(f"Failed to delete event {event_id}")
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Отправляем уведомление через WebSocket
    await ws_manager.broadcast_event("deleted_event", event)
    
    logger.info(f"Event {event_id} deleted successfully")
    return None

@router.get("/repo/{repo_name:path}", response_model=List[RepoEvent])  # Изменено: добавлено :path
async def read_repo_events(
    repo_name: str,
    db: AsyncSession = Depends(get_db_session),
):
    """Получить события по имени репозитория"""
    logger.info(f"GET /events/repo/{repo_name} called")
    events = await EventService.get_events_by_repo(db, repo_name)
    logger.info(f"Returning {len(events)} events for repo {repo_name}")
    return events