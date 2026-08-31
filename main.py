from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import repository

load_dotenv()  # reads your .env file
repository.create_db_and_seed()

app = FastAPI()

class CreateTask(BaseModel):
    title: str

class UpdateTask(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.get("/", summary="API information")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health", summary="Check API health")
def health():
    return {"status": "OK"}

@app.get("/tasks", summary="View all tasks")
def get_tasks():
    return repository.get_all_tasks()

@app.get("/tasks/{task_id}", summary="View a task by ID")
def get_task(task_id: int):
    task = repository.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task

@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task_route(new_task: CreateTask):
    if not new_task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    return repository.create_task(new_task.title)

@app.put("/tasks/{task_id}", summary="Update a task")
def update_task_route(task_id: int, update: UpdateTask):
    if update.title is not None and not update.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    task = repository.update_task(task_id, update.title, update.done)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task

@app.delete("/tasks/{task_id}", status_code=204, summary="Delete task")
def delete_task_route(task_id: int):
    success = repository.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")