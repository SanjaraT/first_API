# Task API

A small CRUD API for managing a to-do list, built with FastAPI. Supports creating, reading, updating, and deleting tasks — no database yet, everything lives in memory.

## What this is

This API lets you manage a list of tasks through HTTP requests. It was built as part of the FlyRank AI internship (Week 2, Assignment BE-01) to practice the core CRUD pattern that shows up in almost every backend.

## How to install & run

```bash
git clone https://github.com/SanjaraT/first_API
cd first_API
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install fastapi uvicorn
uvicorn main:app --reload
```

The server runs at `http://localhost:8000`. Interactive docs are available at `http://localhost:8000/docs`.

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

![Swagger UI screenshot](ui/UI.png)

## Notes

- Data is stored in memory only — restarting the server resets the task list back to the 3 seed tasks. This is intentional for this stage; a real database comes in the following week's assignment.