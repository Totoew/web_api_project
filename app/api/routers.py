from app.api.endpoints import events, tasks

# Список всех роутеров API
routers = [
    events.router,
    tasks.router,
]