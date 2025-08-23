from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass
import threading
import time

# --- Tasks --------------------------------------------
class Task(ABC):
    @abstractmethod
    def execute(self): ...

class PythonTask(Task):
    def execute(self, context: Any):
        print("PythonTask executed")


class JavaScriptTask(Task):
    def execute(self, context: Any):
        print("JavaScriptTask executed")



@dataclass(frozen=True)
class RunResult:
    exit_code: int
    stdout: str
    stderr: str
    image: str
    runtime_ms: int

    def to_dict(self) -> dict:
        return {
            "exit_code": self.exit_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "image": self.image,
            "runtime_ms": self.runtime_ms,
        }

class AbstractDockerRunner(ABC):
    @abstractmethod
    def run(self) -> RunResult: ...


# ----- Receiver ---------------------------------------------------------------
class TaskRunner:
    """Receiver: knows how to run/cancel/retry tasks."""
    def __init__(self):
        self.state: Dict[str, str] = {}  # task_id -> status (e.g., "PENDING", "RUNNING", "DONE", "CANCELLED", "FAILED")

    def run(self, task_id: str) -> str:
        self.state[task_id] = "RUNNING"
        # Simulate work
        time.sleep(0.1)
        self.state[task_id] = "DONE"
        return f"Task {task_id} completed"

    def cancel(self, task_id: str) -> str:
        if self.state.get(task_id) in {"PENDING", "RUNNING"}:
            self.state[task_id] = "CANCELLED"
            return f"Task {task_id} cancelled"
        return f"Task {task_id} not cancellable"

    def retry(self, task_id: str) -> str:
        # If failed, retry; otherwise noop for demo
        if self.state.get(task_id) == "FAILED":
            return self.run(task_id)
        return f"Task {task_id} not in FAILED state"

# ----- Command Interface ------------------------------------------------------
class Command(ABC):
    @abstractmethod
    def execute(self, runner: TaskRunner) -> Any: ...

    def undo(self, runner: TaskRunner) -> None:
        """Optional: not all commands need undo, but we support it when it makes sense."""
        pass

# ----- Concrete Commands ------------------------------------------------------
@dataclass
class FetchDataTaskCommand(Command):
    task_id: str
    _prev_state: Optional[str] = None

    def execute(self, runner: TaskRunner) -> str:
        self._prev_state = runner.state.get(self.task_id)
        return runner.run(self.task_id)

    def undo(self, runner: TaskRunner) -> None:
        # For demo: restore previous state (a lightweight "memento")
        if self._prev_state is None:
            runner.state.pop(self.task_id, None)
        else:
            runner.state[self.task_id] = self._prev_state

@dataclass
class ProcessDataTask(Command):
    task_id: str
    _prev_state: Optional[str] = None

    def execute(self, runner: TaskRunner) -> str:
        self._prev_state = runner.state.get(self.task_id)
        return runner.run(self.task_id)

    def undo(self, runner: TaskRunner) -> None:
        # For demo: restore previous state (a lightweight "memento")
        if self._prev_state is None:
            runner.state.pop(self.task_id, None)
        else:
            runner.state[self.task_id] = self._prev_state

@dataclass
class SaveResultsTask(Command):
    task_id: str
    _prev_state: Optional[str] = None

    def execute(self, runner: TaskRunner) -> str:
        self._prev_state = runner.state.get(self.task_id)
        return runner.run(self.task_id)

    def undo(self, runner: TaskRunner) -> None:
        # For demo: restore previous state (a lightweight "memento")
        if self._prev_state is None:
            runner.state.pop(self.task_id, None)
        else:
            runner.state[self.task_id] = self._prev_state

@dataclass
class DockerTaskCommand(Command):
    name: str
    runner: AbstractDockerRunner
    # optional: info you’ll need for undo / tracing
    output_path: Optional[str] = None  # e.g., where results are saved (mounted volume)

    def execute(self):
        ...
    def undo(self, runner: AbstractDockerRunner):
        ...




