import json
from .base import Command

class ListTasksCommand(Command):
    def __init__(self, file='tasks.json'):
        self.file = file

    def execute(self):
        try:
            with open(self.file, 'r') as f:
                data = json.load(f)
            for i, item in enumerate(data):
                print(f"{i + 1}. {item['task']}")
        except FileNotFoundError:
            print("No tasks found.")