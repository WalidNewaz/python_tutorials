import asyncio
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

@dataclass
class AResult:
    ok: bool
    output: Dict[str, Any]
    error: Optional[str] = None

class AStep:
    name: str
    async def run(self, ctx: Dict[str, Any]) -> AResult: ...

class ASleep(AStep):
    def __init__(self, name: str, seconds: float, key: str, value: Any):
        self.name, self.seconds, self.key, self.value = name, seconds, key, value
    async def run(self, ctx: Dict[str, Any]) -> AResult:
        await asyncio.sleep(self.seconds)
        return AResult(True, {self.key: self.value})

class AParallelGroup(AStep):
    def __init__(self, name: str, steps: List[AStep], *, fail_fast: bool=False):
        self.name, self.steps, self.fail_fast = name, steps, fail_fast

    async def run(self, ctx: Dict[str, Any]) -> AResult:
        tasks = [asyncio.create_task(s.run(ctx.copy())) for s in self.steps]
        results = {}
        errors = []
        for t in asyncio.as_completed(tasks):
            try:
                r: AResult = await t
                if r.ok:
                    results.update(r.output)
                else:
                    errors.append(r.error or "unknown error")
                    if self.fail_fast:
                        for other in tasks:
                            other.cancel()
                        break
            except Exception as e:
                errors.append(str(e))
                if self.fail_fast:
                    for other in tasks:
                        other.cancel()
                    break
        return AResult(not errors, results, " | ".join(errors) if errors else None)

async def demo_async():
    g = AParallelGroup("async-fetch", [
        ASleep("a", 1.0, "A", 1),
        ASleep("b", 0.5, "B", 2),
        ASleep("c", 0.2, "C", 3),
    ])
    res = await g.run({})
    print(res)

asyncio.run(demo_async())