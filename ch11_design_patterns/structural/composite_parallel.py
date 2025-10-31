from dataclasses import dataclass, field
from typing import Protocol, Any, Dict, List, Optional, Callable, Iterable
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, CancelledError, Future

# ---------- Core types ----------

@dataclass
class StepResult:
    ok: bool
    output: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    duration_ms: int = 0

class Step(Protocol):
    name: str
    def run(self, ctx: Dict[str, Any]) -> StepResult: ...

# ---------- Concrete steps (examples) ----------

class SleepStep:
    """Simulates I/O-bound work via sleep; writes a key into context."""
    def __init__(self, name: str, seconds: float, key: str, value: Any):
        self.name = name
        self.seconds = seconds
        self.key = key
        self.value = value

    def run(self, ctx: Dict[str, Any]) -> StepResult:
        start = time.perf_counter()
        try:
            time.sleep(self.seconds)
            return StepResult(True, {self.key: self.value}, duration_ms=int((time.perf_counter()-start)*1000))
        except Exception as e:
            return StepResult(False, error=f"{self.name} failed: {e}", duration_ms=int((time.perf_counter()-start)*1000))

class FailStep:
    def __init__(self, name: str, msg: str = "boom"):
        self.name = name
        self.msg = msg
    def run(self, ctx: Dict[str, Any]) -> StepResult:
        start = time.perf_counter()
        return StepResult(False, error=f"{self.name}: {self.msg}", duration_ms=int((time.perf_counter()-start)*1000))

# ---------- Groups ----------

class SequentialGroup:
    def __init__(self, name: str, steps: List[Step], fail_fast: bool = True):
        self.name = name
        self.steps = steps
        self.fail_fast = fail_fast

    def run(self, ctx: Dict[str, Any]) -> StepResult:
        start = time.perf_counter()
        merged: Dict[str, Any] = {}
        for step in self.steps:
            res = step.run(ctx)
            if res.ok:
                merged.update(res.output)
                ctx.update(res.output)  # option: feed-forward into context
            else:
                if self.fail_fast:
                    return StepResult(False, merged, error=f"[{self.name}] {res.error}",
                                      duration_ms=int((time.perf_counter()-start)*1000))
        return StepResult(True, merged, duration_ms=int((time.perf_counter()-start)*1000))

class ParallelGroup:
    """
    Runs child steps concurrently and merges outputs.
    Options:
      - max_workers: degree of parallelism
      - fail_fast: cancel remaining futures on first failure
      - timeout: optional overall timeout for the group (seconds)
    """
    def __init__(self, name: str, steps: List[Step], *, max_workers: int = 4,
                 fail_fast: bool = False, timeout: Optional[float] = None):
        self.name = name
        self.steps = steps
        self.max_workers = max_workers
        self.fail_fast = fail_fast
        self.timeout = timeout

    def run(self, ctx: Dict[str, Any]) -> StepResult:
        start = time.perf_counter()
        merged: Dict[str, Any] = {}
        errors: List[str] = []

        # Submit all tasks
        with ThreadPoolExecutor(max_workers=self.max_workers, thread_name_prefix=f"{self.name}-") as pool:
            futures: Dict[Future, Step] = {pool.submit(step.run, ctx.copy()): step for step in self.steps}

            try:
                # as_completed supports a timeout per iteration; we implement an overall timeout.
                deadline = (time.perf_counter() + self.timeout) if self.timeout else None
                done_count = 0

                while futures:
                    remaining = self._remaining_time(deadline)
                    # Wait for at least one to finish
                    for fut in as_completed(list(futures.keys()), timeout=remaining):
                        step = futures.pop(fut)
                        try:
                            res: StepResult = fut.result()
                            if res.ok:
                                merged.update(res.output)
                            else:
                                errors.append(res.error or f"{step.name} failed")
                                if self.fail_fast:
                                    # Cancel all remaining futures
                                    for f in futures:
                                        f.cancel()
                                    futures.clear()
                                    raise RuntimeError("fail_fast")
                        except CancelledError:
                            errors.append(f"{step.name} cancelled")
                        except Exception as e:
                            errors.append(f"{step.name} raised: {e}")
                            if self.fail_fast:
                                for f in futures:
                                    f.cancel()
                                futures.clear()
                                raise RuntimeError("fail_fast")

                        done_count += 1

                    # If we set a deadline and exceeded it:
                    if deadline is not None and time.perf_counter() > deadline and futures:
                        for f, st in list(futures.items()):
                            f.cancel()
                            errors.append(f"{st.name} timed out")
                            futures.pop(f, None)
                        break

            except TimeoutError:
                # (per-iteration timeout) defensive—shouldn’t happen with our loop, but safe-guard
                for f, st in futures.items():
                    f.cancel()
                    errors.append(f"{st.name} timed out")
                futures.clear()
            except RuntimeError:
                # fail_fast path already handled cancellation/collect errors
                pass

        duration_ms = int((time.perf_counter() - start) * 1000)
        if errors:
            return StepResult(False, merged, error=f"[{self.name}] " + " | ".join(errors), duration_ms=duration_ms)
        return StepResult(True, merged, duration_ms=duration_ms)

    @staticmethod
    def _remaining_time(deadline: Optional[float]) -> Optional[float]:
        if deadline is None:
            return None
        rem = deadline - time.perf_counter()
        return max(rem, 0.0)


class FnStep:
    def __init__(self, name: str, fn: Callable[[Any, Dict[str, Any]], StepResult], arg: Any):
        self.name = name
        self.fn = fn
        self.arg = arg
    def run(self, ctx: Dict[str, Any]) -> StepResult:
        return self.fn(self.arg, ctx)

class ParallelMap(Step):
    def __init__(
        self, name: str, items: Iterable[Any],
        fn: Callable[[Any, Dict[str, Any]], StepResult],
        *, max_workers: int = 8, timeout: Optional[float] = None
    ):
        self.name = name
        self.items = list(items)
        self.fn = fn
        self.max_workers = max_workers
        self.timeout = timeout

    def run(self, ctx: Dict[str, Any]) -> StepResult:
        # Wrap fn into Steps and delegate to ParallelGroup
        steps = [FnStep(f"{self.name}-{i}", self.fn, item) for i, item in enumerate(self.items)]
        return ParallelGroup(self.name, steps, max_workers=self.max_workers, timeout=self.timeout).run(ctx)


def resize_image(img_path: str, ctx: Dict[str, Any]) -> StepResult:
    # pretend-resize
    time.sleep(0.2)
    return StepResult(True, {f"resized::{img_path}": True})


# ---------- Example Workflow (fan-out / fan-in) ----------

if __name__ == "__main__":
    # Fan-out: 3 independent I/O-ish steps in parallel, then fan-in and continue.
    fetch_in_parallel = ParallelGroup(
        "fetch-assets",
        steps=[
            SleepStep("download-catalog", 1.2, "catalog", {"n": 120}),
            SleepStep("download-prices",  1.0, "prices",  {"currency": "USD"}),
            SleepStep("download-stock",   0.8, "stock",   {"available": True}),
        ],
        max_workers=3,
        fail_fast=False,
        timeout=5.0,
    )

    validate = SequentialGroup("validate", steps=[
        SleepStep("validate-catalog", 0.2, "validated_catalog", True),
        SleepStep("validate-prices",  0.2, "validated_prices",  True),
    ])

    # Full workflow: parallel stage -> sequential stage
    workflow = SequentialGroup("car-assembler-workflow", steps=[
        fetch_in_parallel,
        validate,
        SleepStep("persist", 0.1, "saved", True),
    ])

    ctx: Dict[str, Any] = {}
    result = workflow.run(ctx)

    print("OK:", result.ok)
    print("Duration (ms):", result.duration_ms)
    print("Output keys:", list(result.output.keys()))
    if not result.ok:
        print("Error:", result.error)

# --- With ParallelMap --------------------------
    parallel_resize = ParallelMap("resize-batch", ["a.jpg","b.jpg","c.jpg"], resize_image, max_workers=3)
    # Image resizing workflow
    workflow_img = SequentialGroup("img-resize-workflow", steps=[
        parallel_resize,
        SleepStep("persist", 0.1, "saved", True),
    ])

    ctx: Dict[str, Any] = {}
    result = workflow_img.run(ctx)

    print("OK:", result.ok)
    print("Duration (ms):", result.duration_ms)
    print("Output keys:", list(result.output.keys()))
    if not result.ok:
        print("Error:", result.error)

