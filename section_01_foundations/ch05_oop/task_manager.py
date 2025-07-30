###
### Simple Task Manager
###
import datetime
from typing import List
from task import BaseTask, SimpleTask, DeadlineTask


class TaskManager:
    """
    This class represents a task manager.
    """
    def __init__(self):
        self.tasks = []

    def add_task(self, task: BaseTask):
        self.tasks.append(task)
        return task

    def list_tasks(self):
        """
        Returns a list of all tasks in the task manager.
        :return: A list of the tasks in the task manager.
        """
        return self.tasks

    def get_pending_tasks(self):
        """
        Returns a list of all pending tasks in the task manager.
        :return:
        """
        return [task for task in self.tasks if not task.completed]

    def get_completed_tasks(self):
        """
        Returns a list of all completed tasks in the task manager.
        :return:
        """
        return [task for task in self.tasks if task.completed]

    @staticmethod
    def format_tasks(tasks: List[BaseTask]):
        return [str(task) for task in tasks]

class TaskNotifier:
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager

    def expired_tasks(self):
        return [task for task in self.task_manager.get_pending_tasks() if
                    isinstance(task, DeadlineTask) and task.due_date < datetime.datetime.now()]

if __name__ == "__main__":
    manager = TaskManager()
    notifier = TaskNotifier(manager)

    manager.add_task(SimpleTask("Write unit tests", description="For the task manager application"))
    manager.add_task(SimpleTask("Refactor code"))
    manager.add_task(DeadlineTask("Merge code", due_date=datetime.datetime.now() + datetime.timedelta(days=-1)))

    manager.tasks[0].mark_completed()

    print("\nAll Tasks:")
    print("\n".join(TaskManager.format_tasks(manager.list_tasks())))

    print("\nCompleted Tasks:")
    print("\n".join(TaskManager.format_tasks(manager.get_completed_tasks())))

    print("\nPending Tasks:")
    print("\n".join(TaskManager.format_tasks(manager.get_pending_tasks())))

    print("\nExpired Tasks:")
    print("\n".join(TaskManager.format_tasks(notifier.expired_tasks())))
