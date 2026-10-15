from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#entrada de dados com title, description (optional ser str) e completed(booelan.verificando se foi completa)
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

#output de dados com todos os elements TaskCreate
class Task (TaskCreate):
    id: int
    created_at: datetime

#nome, version
app = FastAPI(
    title="taskfLow API",
    description="API for tasks",
    version="1.0.0",
)

#200
@app.get("/")
def root():
    return {"message": "Hello World"}

#simulação de bd em memória
task_db = []
next_id = 2

#tarefa
Task1 = Task(
    id=1,
    title="Task 1",
    description="Task test",
    completed=True,
    created_at=datetime.now(),
)
#adiciona task 1 a lista do tas_db.
task_db.append(Task1)

@app.get("/tasks")
def tasks():
    return task_db

@app.post("/tasks")
def create_task(task: TaskCreate):
    global next_id
    new_task = Task(
        id=next_id,
        title=task.title,
        description= task.description,
        completed=task.completed,
        created_at=datetime.now(),
    )
    task_db.append(new_task)
    next_id += 1
    return new_task

"""se acessar GET /tasks/1, o task_id recebe 1, percorre task_db, encontra task.id == 1 e 
retorna a task, se percorrer qualuqer outra, 404."""
@app.get("/tasks/{task_id}")
def read_task(task_id: int):
    for task in task_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate):
    for existing_task in task_db:
        if existing_task.id == task_id:
            existing_task.title = task.title
            existing_task.description = task.description
            existing_task.completed = task.completed
            return existing_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for existing_task in task_db:
        if existing_task.id == task_id:
            task_db.remove(existing_task)
            return existing_task
    raise HTTPException(status_code=404, detail="Task not found")
