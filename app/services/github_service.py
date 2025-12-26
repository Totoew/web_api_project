import httpx
from typing import List, Dict, Any
from app.config import settings

class GitHubService:
    def __init__(self):
        self.base_url = settings.github_base_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def fetch_repo_events(self, repo_full_name: str) -> List[Dict[str, Any]]:
        """Получение событий репозитория с GitHub API"""
        url = f"{self.base_url}/repos/{repo_full_name}/events"
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred for {repo_full_name}: {e}")
            return []
        except Exception as e:
            print(f"Error fetching events for {repo_full_name}: {e}")
            return []
    
    async def close(self):
        await self.client.aclose()

# Создаем глобальный экземпляр сервиса
github_service = GitHubService()