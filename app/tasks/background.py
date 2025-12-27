import asyncio
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.services.github_service import github_service
from app.services.event_service import EventService
from app.schemas.repo_event import RepoEventCreate
from app.websocket.ws_manager import ws_manager
from app.nats.publisher import publish_event_created
from app.config import settings

async def fetch_and_process_events():
    """Основная функция фоновой задачи: получение и обработка событий"""
    print(f"[{datetime.now()}] Starting background task...")
    
    async with AsyncSessionLocal() as db:
        for repo_full_name in settings.monitored_repos:
            print(f"Fetching events for {repo_full_name}...")
            
            # Получаем события с GitHub
            events_data = await github_service.fetch_repo_events(repo_full_name)
            
            new_events_count = 0
            for event_data in events_data:
               
                event_create = RepoEventCreate(
                    repo_name=repo_full_name,
                    event_type=event_data.get("type", "UnknownEvent"),
                    actor_login=event_data.get("actor", {}).get("login", "unknown"),
                    created_at=datetime.strptime(
                        event_data.get("created_at"), 
                        "%Y-%m-%dT%H:%M:%SZ"
                    ).replace(tzinfo=timezone.utc),
                    payload=event_data.get("payload", {}),
                    raw_data=event_data
                )
                
                # Сохраняем в БД
                event = await EventService.create_event(db, event_create)
                new_events_count += 1
                
                # Отправляем уведомление через WebSocket
                await ws_manager.broadcast_event("new_event", event)
                
                # Публикуем событие в NATS
                await publish_event_created(event)
                
                # Небольшая задержка, чтобы не перегружать WebSocket/NATS
                await asyncio.sleep(0.01)
            
            print(f"  - {repo_full_name}: fetched {len(events_data)} events, {new_events_count} new")
    
    print(f"[{datetime.now()}] Background task completed.")

async def background_task():
    """Фоновая задача, которая запускается по расписанию"""
    while True:
        try:
            await fetch_and_process_events()
        except Exception as e:
            print(f"Error in background task: {e}")
        
        # Ждем заданный интервал
        await asyncio.sleep(settings.background_task_interval_seconds)

async def manual_fetch_github_events():
    """Ручной запуск задачи (для API endpoint)"""
    await fetch_and_process_events()