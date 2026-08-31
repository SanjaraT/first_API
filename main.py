from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from sqlmodel import SQLModel, Field, create_engine, Session, select

# ----DATABASE----

# task row schema
class Task(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title:str
    done: bool = False

engine = create_engine("sqlite:///tasks.db")

def create_db_and_seed():
    # create the table if missing
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        existing = session.exec(select(Task)).first()
        if not existing:
            session.add(Task(title = "Buy milk", done=False))
            session.add(Task(title = "Walk the dog", done=False))
            session.add(Task(title = "Finish assignment", done=True))
            session.commit()
create_db_and_seed()


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
@app.get("/", summary="API information")
def root():
    return {
        "name":"Task API",
        "version":"1.0",
        "endpoints":["/tasks"]
    }

@app.get("/health", summary="Check API health")
def health():
    return {"status":"OK"}

# task list
@app.get("/tasks", summary="View all tasks")
def get_tasks():
    return tasks

# specific task
@app.get("/tasks/{task_id}", summary="View a task by ID")
def get_task(task_id : int):
    for task in tasks:
        if task ["id"] == task_id:
            return task

    raise HTTPException(status_code=404, detail=f"Task{task_id} not found")


# create new task
@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(new_task: CreateTask):
    if not new_task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    next_id = max((t["id"] for t in tasks), default=0) + 1
    task = {"id": next_id, "title": new_task.title, "done": False}
    tasks.append(task)
    return task

# Update / Edit task
@app.put("/tasks/{task_id}", summary="Update a task")
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
@app.delete("/tasks/{task_id}", status_code=204, summary="Delete task")
def delete_task(task_id : int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return 