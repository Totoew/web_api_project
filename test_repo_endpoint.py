import asyncio
import httpx
import sys
import os
from urllib.parse import quote

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_repo_endpoint():
    print("Testing repo endpoint with different repo names...")
    print("=" * 50)
    
    async with httpx.AsyncClient(base_url="http://localhost:8000", follow_redirects=True) as client:
        # Тестируем разные форматы имен репозиториев
        test_repos = [
            "test/repo",  # То, что мы создали
            "fastapi/fastapi",  # Существующий в БД
            "fastapi",  # Только имя без организации
            "microsoft/vscode",  # Другой существующий
        ]
        
        for repo_name in test_repos:
            print(f"\nTesting repo: {repo_name}")
            
            # Без кодирования
            endpoint = f"/events/repo/{repo_name}"
            print(f"  Endpoint: {endpoint}")
            try:
                response = await client.get(endpoint)
                print(f"  Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"  Number of events: {len(data)}")
                else:
                    print(f"  Response: {response.json()}")
            except Exception as e:
                print(f"  Error: {e}")
            
            # С URL-кодированием
            encoded_repo = quote(repo_name, safe='')
            endpoint = f"/events/repo/{encoded_repo}"
            print(f"  Endpoint (encoded): {endpoint}")
            try:
                response = await client.get(endpoint)
                print(f"  Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"  Number of events: {len(data)}")
                else:
                    print(f"  Response: {response.json()}")
            except Exception as e:
                print(f"  Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_repo_endpoint())