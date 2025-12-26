import json
from typing import Dict, List
from fastapi import WebSocket
from app.schemas.repo_event import WSEventMessage, RepoEvent

class ConnectionManager:
    def __init__(self):
        # Храним активные соединения
        self.active_connections: Dict[str, List[WebSocket]] = {
            "events": []
        }
    
    async def connect(self, websocket: WebSocket, channel: str = "events"):
        """Подключение клиента к WebSocket"""
        await websocket.accept()
        self.active_connections[channel].append(websocket)
        print(f"WebSocket connected. Total connections: {len(self.active_connections[channel])}")
    
    def disconnect(self, websocket: WebSocket, channel: str = "events"):
        """Отключение клиента от WebSocket"""
        if websocket in self.active_connections[channel]:
            self.active_connections[channel].remove(websocket)
            print(f"WebSocket disconnected. Total connections: {len(self.active_connections[channel])}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Отправка сообщения конкретному клиенту"""
        await websocket.send_text(message)
    
    async def broadcast(self, message: str, channel: str = "events"):
        """Рассылка сообщения всем подключенным клиентам канала"""
        disconnected = []
        for connection in self.active_connections[channel]:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error sending message: {e}")
                disconnected.append(connection)
        
        # Удаляем отключенные соединения
        for connection in disconnected:
            self.disconnect(connection, channel)
    
    async def broadcast_event(self, event_type: str, event_data: RepoEvent):
        """Рассылка события в формате JSON всем клиентам"""
        message = WSEventMessage(event_type=event_type, data=event_data)
        await self.broadcast(message.model_dump_json())

# Создаем глобальный экземпляр менеджера
ws_manager = ConnectionManager()