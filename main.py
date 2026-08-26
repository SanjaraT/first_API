from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks = [
    {"id": 1, "title":"Cook lunch", "done":True },
    {"id": 2, "title":"Go outside ", "done":False },
    {"id": 3, "title":"Finish assignment", "done":True },
]

# pydantic schema for creating task
class CreateTask(BaseModel):
    title : str

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