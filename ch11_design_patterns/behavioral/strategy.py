from abc import ABC, abstractmethod
import asyncio
import time


# --- Strategy Interface ---
class ExecutionStrategy(ABC):
    @abstractmethod
    def execute(self, tasks):
        pass


# --- Concrete Strategies ---
class SequentialExecution(ExecutionStrategy):
    def execute(self, tasks):
        print("Running tasks sequentially...")
        start = time.perf_counter()
        results = []
        for task in tasks:
            results.append(task())
        elapsed = time.perf_counter() - start
        return results, elapsed


class ParallelExecution(ExecutionStrategy):
    def execute(self, tasks):
        print("Running tasks in parallel with asyncio...")
        async def runner():
            start = time.perf_counter()
            coroutines = [asyncio.to_thread(task) for task in tasks]
            results = await asyncio.gather(*coroutines)
            elapsed = time.perf_counter() - start
            return results, elapsed

        return asyncio.run(runner())


# --- Context (Workflow Engine) ---
class WorkflowEngine:
    def __init__(self, strategy: ExecutionStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: ExecutionStrategy):
        self.strategy = strategy

    def run(self, tasks):
        return self.strategy.execute(tasks)


# --- Example Tasks ---
def task_a():
    print("Task A running...")
    time.sleep(1)
    return "Result A"

def task_b():
    print("Task B running...")
    time.sleep(2)
    return "Result B"

def task_c():
    print("Task C running...")
    time.sleep(1)
    return "Result C"


# --- Usage Example ---
if __name__ == "__main__":
    usr_tasks = [task_a, task_b, task_c]

    engine = WorkflowEngine(SequentialExecution())
    seq_results, seq_time = engine.run(usr_tasks)
    print(f"Sequential Results: {seq_results}, Time: {seq_time:.2f}s")

    engine.set_strategy(ParallelExecution())
    par_results, par_time = engine.run(usr_tasks)
    print(f"Parallel Results: {par_results}, Time: {par_time:.2f}s")