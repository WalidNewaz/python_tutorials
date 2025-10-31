from abc import ABC, abstractmethod
import asyncio, time
import sys

# --- Strategy interface --------------------------------
class ExecutionStrategy(ABC):
    @abstractmethod
    def execute(self, tasks):
        pass

# --- Concrete strategies --------------------------------
class SequentialStrategy(ExecutionStrategy):
    def execute(self, tasks):
        for task in tasks:
            print(task())
        return "Done sequentially"

class ParallelStrategy(ExecutionStrategy):
    def execute(self, tasks):
        async def runner():
            coroutines = [asyncio.to_thread(task) for task in tasks]
            results = await asyncio.gather(*coroutines)
            print(results)
        asyncio.run(runner())
        return "Done parallel"

class TaskExecutor:
    def __init__(self, strategy: ExecutionStrategy = SequentialStrategy()):
        self.strategy = strategy

    def set_strategy(self, strategy: ExecutionStrategy):
        self.strategy = strategy

    def run(self, tasks):
        return self.strategy.execute(tasks)

# --- tasks --------------------------------
def task_a(): time.sleep(1); return "A"
def task_b(): time.sleep(1); return "B"

ALLOWED_PARAMS = ["sequential", "parallel"]

def get_param() -> str:
    if len(sys.argv) < 2:
        print("Usage: {} [text|json]".format(sys.argv[0]))
        return ""

    param = sys.argv[1]
    if param not in ALLOWED_PARAMS:
        print("Usage: {} [text|json]".format(sys.argv[0]))
        return ""

    return param


def main():
    tasks = [task_a, task_b]

    mode = get_param()
    executor: TaskExecutor

    if mode == "sequential":
        executor = TaskExecutor(SequentialStrategy())
    elif mode == "parallel":
        executor = TaskExecutor(ParallelStrategy())
    else:
        raise ValueError("Invalid mode")

    result = executor.run(tasks)
    print(result)

if __name__ == "__main__":
    main()
