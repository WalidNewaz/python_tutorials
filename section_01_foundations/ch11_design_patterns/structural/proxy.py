# The **Proxy Pattern** provides a surrogate or placeholder object
# that controls access to another object. Instead of calling the
# real object directly, clients interact with the proxy, which decides
# how and when to delegate requests.

from abc import ABC, abstractmethod


class Task(ABC):
    """Abstract base class for workflow tasks."""

    @abstractmethod
    def execute(self, user: str) -> str:
        """Execute the task with the given user context."""
        raise NotImplementedError


class RealTask(Task):
    """The real implementation of a workflow task."""

    def __init__(self, name: str) -> None:
        self.name = name

    def execute(self, user: str) -> str:
        return f"Task '{self.name}' executed by {user}..."


class TaskProxy(Task):
    """Proxy for Task that enforces role-based access."""

    def __init__(self, real_task: RealTask, allowed_roles: list[str]) -> None:
        self._real_task = real_task
        self._allowed_roles = allowed_roles

    def execute(self, user: str, role: str | None = None) -> str:
        if role not in self._allowed_roles:
            return f"Access denied for {user} with role={role}!"
        return self._real_task.execute(user)

if __name__ == "__main__":
    approve_payment = RealTask("Approve Payment")
    proxy = TaskProxy(approve_payment, allowed_roles=["Manager", "Admin"])

    print(proxy.execute("Alice", role="Employee"))
    print(proxy.execute("Bob", role="Manager"))