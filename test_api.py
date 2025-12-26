import asyncio
import httpx
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_api():
    print("Testing API endpoints...")
    print("=" * 50)
    
    async with httpx.AsyncClient(base_url="http://localhost:8000", follow_redirects=True) as client:
        # Тест 1: Корневой эндпоинт
        print("1. Testing root endpoint...")
        try:
            response = await client.get("/")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Тест 2: Получение событий (пробуем с разными вариантами)
        print("\n2. Testing GET /events...")
        for endpoint in ["/events", "/events/", "/events?limit=5", "/events/?limit=5"]:
            try:
                response = await client.get(endpoint)
                print(f"   Endpoint: {endpoint}")
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"   Number of events: {len(data)}")
                    if data:
                        print(f"   First event ID: {data[0].get('id', 'No ID')}")
                elif response.status_code != 200:
                    print(f"   Response text: {response.text[:100]}")
                print()
            except Exception as e:
                print(f"   Error: {e}")
        
        # Тест 3: Создание тестового события
        print("\n3. Testing POST /events...")
        try:
            test_event = {
                "repo_name": "test/repo",
                "event_type": "TestEvent",
                "actor_login": "testuser",
                "created_at": "2023-12-26T19:00:00Z",
                "payload": {"test": "data"}
            }
            response = await client.post("/events", json=test_event)
            print(f"   Status: {response.status_code}")
            if response.status_code == 201:
                print(f"   Created event ID: {response.json().get('id')}")
            elif response.status_code != 201:
                print(f"   Response text: {response.text[:100]}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Тест 4: Получение событий по репозиторию
        print("\n4. Testing GET /events/repo/test/repo...")
        try:
            response = await client.get("/events/repo/test/repo")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Number of events: {len(data)}")
            else:
                print(f"   Response: {response.json()}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Тест 5: Проверка health endpoint
        print("\n5. Testing GET /health...")
        try:
            response = await client.get("/health")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
        except Exception as e:
            print(f"   Error: {e}")
    
    print("=" * 50)
    print("API test completed!")

if __name__ == "__main__":
    asyncio.run(test_api())