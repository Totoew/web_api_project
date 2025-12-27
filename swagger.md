**Swagger-документация для проекта GitHub Monitor API**

---

## **GitHub Monitor API - Swagger Documentation**

### **Base URL**
```
http://localhost:8000
```

### **Authentication**
No authentication required for this API.

---

## **Health & Info Endpoints**

### **GET /**
**Summary:** Get API information  
**Description:** Returns basic information about the API service  
**Responses:**
- `200`: Successful response
  ```json
  {
    "message": "GitHub Monitor API",
    "docs": "/docs",
    "websocket": "/ws/events",
    "monitored_repos": [
      "fastapi/fastapi",
      "python/cpython", 
      "microsoft/vscode"
    ]
  }
  ```

### **GET /health**
**Summary:** Health check  
**Description:** Check service health and NATS connection status  
**Responses:**
- `200`: Service is healthy
  ```json
  {
    "status": "healthy",
    "nats_connected": true
  }
  ```

---

## **Events Management**

### **GET /events/**
**Summary:** Get list of events  
**Description:** Retrieve GitHub events with pagination  
**Parameters:**
- `skip` (query, integer, optional): Number of records to skip. Default: 0
- `limit` (query, integer, optional): Maximum number of records to return. Default: 100, Maximum: 1000

**Responses:**
- `200`: Successful response
  ```json
  [
    {
      "id": "uuid-string",
      "repo_name": "owner/repo",
      "event_type": "PushEvent",
      "actor_login": "username",
      "created_at": "2023-12-27T10:00:00Z",
      "payload": {}
    }
  ]
  ```

### **GET /events/{event_id}**
**Summary:** Get specific event  
**Description:** Retrieve a single GitHub event by ID  
**Parameters:**
- `event_id` (path, string, required): Event UUID

**Responses:**
- `200`: Event found
  ```json
  {
    "id": "uuid-string",
    "repo_name": "owner/repo",
    "event_type": "PushEvent",
    "actor_login": "username",
    "created_at": "2023-12-27T10:00:00Z",
    "payload": {}
  }
  ```
- `404`: Event not found
  ```json
  {
    "detail": "Event not found"
  }
  ```

### **POST /events/**
**Summary:** Create new event  
**Description:** Manually create a GitHub event  
**Request Body:**
```json
{
  "repo_name": "string (required)",
  "event_type": "string (required)",
  "actor_login": "string (optional)",
  "created_at": "string (ISO 8601 datetime, required)",
  "payload": "object (optional)"
}
```

**Example Request:**
```json
{
  "repo_name": "test/repo",
  "event_type": "TestEvent",
  "actor_login": "testuser",
  "created_at": "2023-12-27T10:00:00Z",
  "payload": {"test": "data"}
}
```

**Responses:**
- `201`: Event created successfully
  ```json
  {
    "id": "uuid-string",
    "repo_name": "test/repo",
    "event_type": "TestEvent",
    "actor_login": "testuser",
    "created_at": "2023-12-27T10:00:00Z",
    "payload": {"test": "data"}
  }
  ```

### **DELETE /events/{event_id}**
**Summary:** Delete event  
**Description:** Delete a GitHub event by ID  
**Parameters:**
- `event_id` (path, string, required): Event UUID

**Responses:**
- `204`: Event deleted successfully (no content)
- `404`: Event not found
  ```json
  {
    "detail": "Event not found"
  }
  ```

### **GET /events/repo/{repo_name}**
**Summary:** Get events by repository  
**Description:** Retrieve GitHub events for a specific repository  
**Parameters:**
- `repo_name` (path, string, required): Repository name (supports slashes, e.g., "fastapi/fastapi")

**Responses:**
- `200`: Successful response
  ```json
  [
    {
      "id": "uuid-string",
      "repo_name": "owner/repo",
      "event_type": "PushEvent",
      "actor_login": "username",
      "created_at": "2023-12-27T10:00:00Z",
      "payload": {}
    }
  ]
  ```

---

## **Tasks Management**

### **POST /tasks/run**
**Summary:** Run background task manually  
**Description:** Force start the background task that fetches data from GitHub API  
**Responses:**
- `200`: Task started successfully
  ```json
  {
    "message": "Фоновая задача запущена вручную",
    "status": "started"
  }
  ```

---

## **WebSocket**

### **WebSocket Endpoint**
```
ws://localhost:8000/ws/events
```

### **Connection**
Client connects to WebSocket endpoint and receives real-time notifications.

### **Message Format**
**From server to client:**
```json
{
  "event_type": "new_event",
  "data": {
    "id": "uuid-string",
    "repo_name": "owner/repo",
    "event_type": "PushEvent",
    "actor_login": "username",
    "created_at": "2023-12-27T10:00:00Z",
    "payload": {}
  }
}
```

**Event types:**
- `new_event`: When a new event is created
- `deleted_event`: When an event is deleted

**From client to server:**
Any text message (e.g., "ping") for connection testing.

---

## **Models/Schemas**

### **RepoEvent (Response Model)**
```json
{
  "id": "string (UUID)",
  "repo_name": "string",
  "event_type": "string",
  "actor_login": "string | null",
  "created_at": "string (ISO 8601 datetime)",
  "payload": "object | null"
}
```

### **RepoEventCreate (Request Model)**
```json
{
  "repo_name": "string (required)",
  "event_type": "string (required)",
  "actor_login": "string | null",
  "created_at": "string (ISO 8601 datetime, required)",
  "payload": "object | null"
}
```

---

## **Monitoring**

### **NATS Integration**
- **Channel:** `github.events` - Events are published here
- **Channel:** `github.commands` - Commands can be sent here (e.g., `{"command": "update_now"}`)

### **Monitor URLs:**
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **NATS Web UI:** http://localhost:8222

---

## **Background Task**

### **Automatic Execution**
- **Interval:** Every 5 minutes (300 seconds)
- **Monitored Repositories:**
  1. `fastapi/fastapi`
  2. `python/cpython`
  3. `microsoft/vscode`

### **Task Workflow:**
1. Fetch events from GitHub API for each repository
2. Process and store new events in database
3. Send WebSocket notifications to connected clients
4. Publish events to NATS channel `github.events`

### **Manual Trigger:**
```bash
POST /tasks/run
```

---

## **Error Responses**

### **HTTP 404 - Not Found**
```json
{
  "detail": "Event not found"
}
```

### **HTTP 422 - Validation Error**
```json
{
  "detail": [
    {
      "loc": ["body", "repo_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```