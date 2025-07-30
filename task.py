from abc import ABC, abstractmethod

class BaseTask:
    @abstractmethod
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.completed = False

    @abstractmethod
    def mark_completed(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

class SimpleTask(BaseTask):
    def __init__(self, name, description=""):
        super().__init__(name, description)
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "Done" if self.completed else "Pending"
        return f"[{status}] {self.name}{ ": " + self.description if len(self.description) > 0 else "" }"

    def __repr__(self):
        status = "Done" if self.completed else "Pending"
        return f"[{status}] {self.name}{ ": " + self.description if len(self.description) > 0 else "" }"

class DeadlineTask(BaseTask):
    def __init__(self, name, description="", due_date=None):
        super().__init__(name, description)
        self.completed = False
        self.due_date = due_date

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "Done" if self.completed else "Pending"
        return f"[{status}] {self.name}{": " + self.description if len(self.description) > 0 else ""}, Due Date: {self.due_date}"

    def __repr__(self):
        status = "Done" if self.completed else "Pending"
        return f"[{status}] {self.name}{": " + self.description if len(self.description) > 0 else ""}, Due Date: {self.due_date}"
