from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import queue
import threading
import time


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
class RunTaskCommand(Command):
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
class CancelTaskCommand(Command):
    task_id: str
    _prev_state: Optional[str] = None

    def execute(self, runner: TaskRunner) -> str:
        self._prev_state = runner.state.get(self.task_id)
        return runner.cancel(self.task_id)

    def undo(self, runner: TaskRunner) -> None:
        if self._prev_state is None:
            runner.state.pop(self.task_id, None)
        else:
            runner.state[self.task_id] = self._prev_state


@dataclass
class RetryTaskCommand(Command):
    task_id: str
    _prev_state: Optional[str] = None

    def execute(self, runner: TaskRunner) -> str:
        self._prev_state = runner.state.get(self.task_id)
        return runner.retry(self.task_id)

    def undo(self, runner: TaskRunner) -> None:
        if self._prev_state is None:
            runner.state.pop(self.task_id, None)
        else:
            runner.state[self.task_id] = self._prev_state


# ----- Macro (Composite) Command ---------------------------------------------
@dataclass
class MacroCommand(Command):
    commands: List[Command]

    def execute(self, runner: TaskRunner) -> List[Any]:
        results = []
        for cmd in self.commands:
            results.append(cmd.execute(runner))
        return results

    def undo(self, runner: TaskRunner) -> None:
        # Undo in reverse order
        for cmd in reversed(self.commands):
            cmd.undo(runner)


# ----- Invoker: CommandBus ----------------------------------------------------
class CommandBus:
    """Invoker: can execute commands now, or enqueue them for worker threads."""
    def __init__(self, runner: TaskRunner):
        self.runner = runner
        self.history: List[Command] = []
        self.q: "queue.Queue[Command]" = queue.Queue()
        self._stop = threading.Event()
        self._worker: Optional[threading.Thread] = None

    # Immediate execution (returns result)
    def dispatch(self, cmd: Command) -> Any:
        result = cmd.execute(self.runner)
        self.history.append(cmd)
        return result

    # Enqueue for background worker
    def enqueue(self, cmd: Command) -> None:
        self.q.put(cmd)

    def start_worker(self) -> None:
        if self._worker and self._worker.is_alive():
            return

        def worker():
            while not self._stop.is_set():
                try:
                    cmd = self.q.get(timeout=0.1)
                except queue.Empty:
                    continue
                cmd.execute(self.runner)
                self.history.append(cmd)
                self.q.task_done()

        self._worker = threading.Thread(target=worker, daemon=True)
        self._worker.start()

    def stop_worker(self) -> None:
        self._stop.set()
        if self._worker:
            self._worker.join(timeout=1)

    def undo_last(self) -> None:
        if not self.history:
            return
        cmd = self.history.pop()
        cmd.undo(self.runner)

# ----- Usage ------------------------------------------------------------------
if __name__ == "__main__":
    task_runner = TaskRunner()
    bus = CommandBus(task_runner)

    # Immediate execution
    print(bus.dispatch(RunTaskCommand("task-1")))     # -> Task task-1 completed
    print(bus.dispatch(CancelTaskCommand("task-1")))  # -> Task task-1 cancelled

    # Undo the last action (cancel)
    bus.undo_last()
    print("State after undo:", task_runner.state["task-1"])  # Restored state

    # Batch/macro (e.g., mass operations)
    macro = MacroCommand([
        RunTaskCommand("job-100"),
        RunTaskCommand("job-101"),
        CancelTaskCommand("job-100"),
    ])
    print(bus.dispatch(macro))  # list of results

    # Queue + background worker
    bus.start_worker()
    for i in range(3):
        bus.enqueue(RunTaskCommand(f"job-{i}"))
    bus.q.join()
    bus.stop_worker()

    print("Final state:", task_runner.state)