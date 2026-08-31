from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv() 
DATABASE_URL = os.getenv("DATABASE_URL")

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    done: bool = False

engine = create_engine(DATABASE_URL)

def create_db_and_seed():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        existing = session.exec(select(Task)).first()
        if not existing:
            session.add(Task(title="Buy milk", done=False))
            session.add(Task(title="Walk the dog", done=False))
            session.add(Task(title="Finish assignment", done=True))
            session.commit()

def get_all_tasks():
    with Session(engine) as session:
        return session.exec(select(Task)).all()

def get_task_by_id(task_id: int):
    with Session(engine) as session:
        return session.get(Task, task_id)

def create_task(title: str):
    with Session(engine) as session:
        task = Task(title=title, done=False)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

def update_task(task_id: int, title: Optional[str], done: Optional[bool]):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            return None
        if title is not None:
            task.title = title
        if done is not None:
            task.done = done
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

def delete_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            return False
        session.delete(task)
        session.commit()
        return True