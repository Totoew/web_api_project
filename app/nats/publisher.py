import json
from app.services.nats_service import nats_client
from app.config import settings
from app.schemas.repo_event import RepoEvent

async def publish_event_created(event: RepoEvent):
    """Публикация события в NATS"""
    if nats_client.is_connected:
        try:
            # Подготавливаем данные для отправки
            event_data = {
                "type": "event_created",
                "timestamp": event.created_at.isoformat(),
                "data": {
                    "id": event.id,
                    "repo_name": event.repo_name,
                    "event_type": event.event_type,
                    "actor_login": event.actor_login,
                }
            }
            
            # Публикуем в канал
            await nats_client.publish(
                settings.nats_events_channel,
                json.dumps(event_data)
            )
            print(f"Event published to NATS: {event.id}")
        except Exception as e:
            print(f"Error publishing to NATS: {e}")

async def publish_task_started():
    """Публикация события запуска задачи"""
    if nats_client.is_connected:
        try:
            import asyncio
            task_data = {
                "type": "task_started",
                "timestamp": asyncio.get_event_loop().time(),
                "data": {"status": "started"}
            }
            await nats_client.publish(
                settings.nats_events_channel,
                json.dumps(task_data)
            )
        except Exception as e:
            print(f"Error publishing task status: {e}")