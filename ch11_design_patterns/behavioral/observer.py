# The **Observer Pattern** is a **behavioral design pattern** where an object,
# called the **Subject**, maintains a list of dependents, called **Observers**,
# and automatically **notifies them of state changes**.

from abc import ABC, abstractmethod


# --- Subject (Publisher) ---
class WorkflowTask:
    def __init__(self, name: str):
        self.name = name
        self._observers = []

    def attach(self, observer: "Observer"):
        self._observers.append(observer)

    def detach(self, observer: "Observer"):
        self._observers.remove(observer)

    def notify(self, status: str):
        for observer in self._observers:
            observer.update(self.name, status)

    def run(self):
        print(f"️Running task: {self.name}")
        # Simulate execution
        self.notify("started")
        self.notify("completed")


# --- Observer Interface ---
class Observer(ABC):
    @abstractmethod
    def update(self, task_name: str, status: str):
        pass


# --- Concrete Observers ---
class LoggerObserver(Observer):
    def update(self, task_name: str, status: str):
        print(f"[Logger] Task {task_name} -> {status}")


class UIObserver(Observer):
    def update(self, task_name: str, status: str):
        print(f"[UI] Updating dashboard: Task {task_name} is {status}")


class AlertObserver(Observer):
    def update(self, task_name: str, status: str):
        """
        Only updates when the status is `completed`; skips otherwise.
        """
        if status == "completed":
            print(f"[Alert] Task {task_name} finished successfully!")


# --- Usage Example ---
if __name__ == "__main__":
    task = WorkflowTask("Data Ingestion")

    # Attach observers
    task.attach(LoggerObserver())
    task.attach(UIObserver())
    task.attach(AlertObserver())

    # Run task
    task.run()
