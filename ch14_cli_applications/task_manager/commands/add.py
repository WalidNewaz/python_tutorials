import json
from .base import Command

class AddTaskCommand(Command):
    def __init__(self, task, file='tasks.json'):
        self.task = task
        self.file = file

    def execute(self):
        try:
            with open(self.file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        data.append({"task": self.task})
        with open(self.file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Task added: {self.task}")