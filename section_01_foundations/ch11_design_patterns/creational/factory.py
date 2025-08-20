from abc import ABC, abstractmethod


class Task(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError("Subclasses must implement the 'run' method.")


class HttpTask(Task):
    def __init__(self, *params, **kwargs):
        self.kwargs = kwargs
        self.params = params
        super().__init__()

    def run(self):
        print("Starting HTTP request...")
        print(self.params, self.kwargs)


class SqlTask(Task):
    def __init__(self, *params, **kwargs):
        self.kwargs = kwargs
        self.params = params
        super().__init__()

    def run(self):
        print("Starting SQL request...")
        print(self.params, self.kwargs)


class SparkTask(Task):
    def __init__(self, *params, **kwargs):
        self.kwargs = kwargs
        self.params = params
        super().__init__()

    def run(self):
        print("Starting Spark request...")
        print(self.params, self.kwargs)


class TaskFactory:
    _registry = {
        "http": HttpTask,
        "sql": SqlTask,
        "spark": SparkTask,
    }

    @classmethod
    def create(cls, spec: dict) -> Task:
        kind = spec["type"]
        return cls._registry[kind](**spec["params"])


task1 = TaskFactory.create({'type': "http", 'params': {'url': 'https://www.google.com'}})
task1.run()
task2 = TaskFactory.create({'type': "sql", 'params': {'query': 'SELECT * FROM USERS'}})
task2.run()
