import json

import requests

from main import Task
response = requests.get("http://127.0.0.1:8000/tasks")
json_data = json.loads(response.text)
task_db = response.json()
print(task_db)

#mandar resquest
new_task = {
    "title: ": "novo teste",
    "description: ": "teste",
    "completed: ": True,
}
