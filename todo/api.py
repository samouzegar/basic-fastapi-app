from todo.server import server
from todo.schemas import ListTasksSchema

TODO = []

@server.get('/todo', response_model=ListTasksSchema)
def get_tasks():
    return {
        'tasks': TODO
    }