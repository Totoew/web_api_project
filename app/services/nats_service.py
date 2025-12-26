import asyncio
import json
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout
from app.config import settings

class NATSClient:
    def __init__(self):
        self.nc = NATS()
        self.is_connected = False
        self._subscription = None
    
    async def connect(self):
        """Подключение к серверу NATS"""
        try:
            await self.nc.connect(
                servers=[settings.nats_url],
                reconnect_time_wait=5,
                max_reconnect_attempts=-1,  # Бесконечные попытки переподключения
                name="github-monitor"
            )
            self.is_connected = True
            print(f"Connected to NATS at {settings.nats_url}")
        except Exception as e:
            print(f"Failed to connect to NATS: {e}")
            self.is_connected = False
    
    async def close(self):
        """Закрытие соединения с NATS"""
        if self.is_connected:
            await self.nc.drain()
            self.is_connected = False
            print("NATS connection closed")
    
    async def publish(self, subject: str, message: str):
        """Публикация сообщения в NATS"""
        if self.is_connected:
            try:
                await self.nc.publish(subject, message.encode())
            except Exception as e:
                print(f"Error publishing to NATS: {e}")
    
    async def subscribe(self, subject: str, callback):
        """Подписка на канал NATS с callback-функцией"""
        if self.is_connected:
            try:
                self._subscription = await self.nc.subscribe(subject, cb=callback)
                print(f"Subscribed to NATS channel: {subject}")
                return self._subscription
            except Exception as e:
                print(f"Error subscribing to NATS: {e}")
                return None

# Глобальный экземпляр клиента NATS
nats_client = NATSClient()