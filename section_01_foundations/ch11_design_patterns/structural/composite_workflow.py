from abc import ABC, abstractmethod
from typing import Any, List

# 1) Component
class Task(ABC):
    @abstractmethod
    def run(self) -> Any: ...

# 2) Leaf Task
class PrintTask(Task):
    def __init__(self, message: str):
        self.message = message

    def run(self) -> str:
        # Side-effect could be logging, HTTP call, etc.
        output = f"[PrintTask] {self.message}"
        print(output)
        return output

# Another leaf
class AddTask(Task):
    def __init__(self, a: int, b: int):
        self.a, self.b = a, b

    def run(self) -> int:
        return self.a + self.b

# 3) Composite (sequence of tasks)
class TaskGroup(Task):
    def __init__(self, name: str):
        self.name = name
        self._children: List[Task] = []

    def add(self, task: Task) -> None:
        self._children.append(task)

    def remove(self, task: Task) -> None:
        self._children.remove(task)

    def run(self) -> List[Any]:
        results = []
        print(f"[TaskGroup] Starting: {self.name}")
        for t in self._children:
            results.append(t.run())
        print(f"[TaskGroup] Finished: {self.name}")
        return results

# ---- Usage ---------------------------------------------------------
if __name__ == "__main__":
    t1 = PrintTask("Validate input")
    t2 = AddTask(40, 2)
    t3 = PrintTask("Persist to DB")

    sub_pipeline = TaskGroup("Preprocess")
    sub_pipeline.add(t1)
    sub_pipeline.add(t2)

    pipeline = TaskGroup("Main Workflow")
    pipeline.add(sub_pipeline)
    pipeline.add(t3)

    all_results = pipeline.run()
    print("Results:", all_results)