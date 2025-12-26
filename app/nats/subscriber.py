import json
from app.services.nats_service import nats_client
from app.config import settings
from app.tasks.background import manual_fetch_github_events

async def handle_nats_message(msg):  # Обратите внимание: handle_nats_message (без s)
    """Callback-функция для обработки сообщений из NATS"""
    try:
        data = json.loads(msg.data.decode())
        print(f"Received NATS message on {msg.subject}: {data}")
        
        # Обрабатываем команды
        if data.get("command") == "update_now":
            print("Manual update requested via NATS")
            await manual_fetch_github_events()
        
    except json.JSONDecodeError as e:
        print(f"Error decoding NATS message: {e}")
    except Exception as e:
        print(f"Error processing NATS message: {e}")

async def start_nats_subscriber():
    """Запуск подписчика NATS"""
    if nats_client.is_connected:
        await nats_client.subscribe(settings.nats_commands_channel, handle_nats_message)  # передаем handle_nats_message