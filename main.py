from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

tasks = [
    {"id": 1, "title":"Cook lunch", "done":True },
    {"id": 2, "title":"Go outside ", "done":False },
    {"id": 3, "title":"Finish assignment", "done":True },
]

# pydantic schema for creating task
class CreateTask(BaseModel):
    title : str

# shema for update
class UpdateTask(BaseModel):
    title : Optional[str] = None
    done : Optional[bool] = None


# status
@app.get("/")
def root():
    return {
        "name":"Task API",
        "version":"1.0",
        "endpoints":["/tasks"]
    }

@app.get("/health")
def health():
    return {"status":"OK"}

# task list
@app.get("/tasks")
def get_tasks():
    return tasks

# specific task
@app.get("/tasks/{task_id}")
def get_task(task_id : int):
    for task in tasks:
        if task ["id"] == task_id:
            return task

    raise HTTPException(status_code=404, detail=f"Task{task_id} not found")


# create new task
@app.post("/tasks", status_code=201)
def create_task(new_task: CreateTask):
    if not new_task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    next_id = max((t["id"] for t in tasks), default=0) + 1
    task = {"id": next_id, "title": new_task.title, "done": False}
    tasks.append(task)
    return task

# Update / Edit task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, update : UpdateTask):
    for task in tasks:
        if task["id"] == task_id:
            if update.title is not None:
                if not update.title.strip():
                    raise HTTPException(status_code=400, detail = "Title cannot be empty")
                task["title"] = update.title
            if update.done is not None:
                task["done"] = update.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


# delete  task
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id : int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return 