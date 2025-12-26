import asyncio
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

# Простое приложение для проверки
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "GitHub Monitor API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("Starting simple test server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)