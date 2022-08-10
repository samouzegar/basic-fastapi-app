import uuid
from starlette import status
from datetime import datetime

from todo.server import server
from todo.schemas import ListTasksSchema, GetTaskSchema, CreateTaskSchema

from fastapi import HTTPException


TODO = []

@server.get('/todo', response_model=ListTasksSchema)
def get_tasks():
    return {
        'tasks': TODO
    }


@server.post('/todo', response_model=GetTaskSchema, status_code=status.HTTP_201_CREATED)
def create_task(payload: CreateTaskSchema):
    task = payload.dict()
    task['id'] = uuid.uuid4()
    task['created'] = datetime.now()
    task['status'] = task['status']
    task['priority'] = task['priority']
    TODO.append(task)
    return task


@server.get('/todo/{task_id}', response_model=GetTaskSchema)
def get_task(task_id: uuid.UUID):
    for task in TODO:
        if task['id'] == task_id:
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with task id {task_id} not found')


@server.put('/todo/{task_id}', response_model=GetTaskSchema)
def update_task(task_id: uuid.UUID, payload: CreateTaskSchema):
    new_task = payload.dict()
    for task in TODO:
        if task['id'] == task_id:
            task.update(new_task)
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with task id {task_id} not found')

@server.delete('/todo/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: uuid.UUID):
    for idx, task in enumerate(TODO):
        if task['id'] == task_id:
            TODO.pop(idx)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with task id {task_id} not found')