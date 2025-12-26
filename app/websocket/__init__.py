from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.ws_manager import ws_manager

router = APIRouter()

@router.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint для получения обновлений о событиях"""
    await ws_manager.connect(websocket)
    
    try:
        # Бесконечный цикл для поддержания соединения
        while True:
            # Ожидаем сообщение от клиента (можно использовать для heartbeat)
            data = await websocket.receive_text()
            # Можно обрабатывать команды от клиента, если нужно
            print(f"Message from client: {data}")
            
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket)