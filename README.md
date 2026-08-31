# Task API

A small CRUD API for managing a to-do list, built with FastAPI. Supports creating, reading, updating, and deleting tasks — data is stored persistently in a SQLite database.

## What this is

This API lets you manage a list of tasks through HTTP requests. It was built as part of the FlyRank AI internship Assignment BE-01 (CRUD basics) and W3 · A1 (connecting to a real database) to practice the core CRUD pattern that shows up in almost every backend, and the separation between an API and its storage layer.

## How to install & run

```bash
git clone https://github.com/SanjaraT/first_API
cd first_API
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install fastapi uvicorn sqlmodel
uvicorn main:app --reload
```

The server runs at `http://localhost:8000`. Interactive docs are available at `http://localhost:8000/docs`.

## Database

- **Why SQLite:** it needs no separate server or installation — the whole database lives in a single file, which is ideal for a small project like this while still using real SQL underneath.
- **Where it lives:** `tasks.db`, created automatically in the project root the first time the app runs. The `tasks` table is created automatically if it doesn't exist, and is seeded with 3 example tasks only on the very first run — restarting the server no longer resets your data.

## Endpoints

| Method | Path            | Description                     | Success | Errors                     |
|--------|-----------------|----------------------------------|---------|-----------------------------|
| GET    | `/`             | API info                        | 200     | —                           |
| GET    | `/health`       | Health check                    | 200     | —                           |
| GET    | `/tasks`        | List all tasks                  | 200     | —                           |
| GET    | `/tasks/{id}`   | Get a single task                | 200     | 404 if id not found        |
| POST   | `/tasks`        | Create a new task                | 201     | 400 if title missing/empty |
| PUT    | `/tasks/{id}`   | Update a task's title and/or done| 200     | 400 invalid body · 404 unknown id |
| DELETE | `/tasks/{id}`   | Delete a task                    | 204     | 404 if id not found        |

## Example request

```bash
Invoke-WebRequest -Uri http://localhost:8000/tasks -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"title":"Buy milk"}'
```

```
StatusCode        : 201
StatusDescription : Created
Content           : {"id":4,"title":"Buy milk","done":false}
RawContent        : HTTP/1.1 201 Created
                    Content-Length: 40
                    Content-Type: application/json
                    Date: Wed, 26 Aug 2026 13:27:04 GMT
                    Server: uvicorn
                    
                    {"id":4,"title":"Buy milk","done":false}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 40
```

## Swagger UI

The full CRUD cycle was tested via `/docs` using "Try it out" for each endpoint.

![Swagger UI screenshot](screenshots/UI.PNG)

## Exploring the database directly

Opened `tasks.db` in DB Browser for SQLite and ran queries directly against the table, confirming the API reflects manual database changes immediately. Example query:

```sql
SELECT * FROM tasks WHERE done = 1;
```

![Database viewer screenshot](screenshots/sql.PNG)

## Notes

- Data now persists in `tasks.db` (SQLite) , restarting the server no longer resets the task list. The 3 example tasks are only inserted once, the first time the database is created.
- Earlier version of this project stored tasks in memory only (a plain Python list); this was replaced with SQLite while keeping every API endpoint identical , proving that storage is an implementation detail behind the API, not part of the API's contract.