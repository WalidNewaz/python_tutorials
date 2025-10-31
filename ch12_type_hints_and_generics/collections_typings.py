# Good parameter types: accept any sequence/mapping; return concrete types.
from collections.abc import Sequence, Mapping, MutableMapping, Iterable, Iterator
from typing import TypedDict, NamedTuple, Generator

def average(nums: Sequence[float]) -> float:
    return sum(nums) / len(nums)

def invert(d: Mapping[str, int]) -> dict[int, str]:
    return {v: k for k, v in d.items()}

# `Mapping[K, V]` (read‑only) vs `MutableMapping[K, V]`
def touch(cache: MutableMapping[str, int], key: str) -> None:
    cache[key] = cache.get(key, 0) + 1

# type aliasing
Matrix = list[list[float]]               # 2D list
AdjList = dict[str, set[str]]            # graph adjacency list
Records = list[tuple[int, str | None]]   # union in tuples (3.10+ `|` syntax)

# Typed dictionaries
class UserTD(TypedDict):
    id: int
    name: str
    email: str | None

class Point(NamedTuple):
    x: float
    y: float

def make_user() -> UserTD:
    return {"id": 1, "name": "Alice", "email": None}

def make_point() -> Point:
    return Point(1, 2)

# Iterators and generators
def only_ints(xs: Iterable[int]) -> list[int]:
    return [x for x in xs if isinstance(x, int)]

def countdown(n: int) -> Iterator[int]:
    while n:
        yield n
        n -= 1

# A Coroutine with send()
def running_average() -> Generator[float, float, None]:
    total = 0.0
    count = 0
    avg = 0.0
    while True:
        new_value = yield avg   # Yields the current average
        total += new_value      # Accepts values from .send()
        count += 1
        avg = total / count

def accumulate(limit: int) -> Generator[int, None, int]:
    total = 0
    for item in range(limit):
        yield item
        total += item
    return total

# --- Tests --------------------------------

values: list[float] = [1.0, 2.0, 3.5]
print(average(values))  # 2.166...

my_cache: MutableMapping[str, int] = {}
touch(my_cache, "key")
print(my_cache)
touch(my_cache, "key")
print(my_cache)
touch(my_cache, "another-key")
print(my_cache)

# Test type aliasing
my_matrix: Matrix = [[1.2, 3.3, 9.5], [8.7, 4.5, 5.6]]
print(my_matrix)
adjacency: AdjList = { 'one': { '1', '2', '3'}, 'two': { '1', '2', '3'} }
print(adjacency)
my_rec: Records = [(1, 'one'), (2, 'two'), (3, 'three')]
print(my_rec)

# Test typed dicts
print(make_user())
print(make_point())

# Test iterators and generators
for i in only_ints([11, 12, 13]):
    print(i)

for i in countdown(10):
    print(i)

avg_gen = running_average()
print(next(avg_gen))       # Prime the generator → 0.0
print(avg_gen.send(10.0))  # send(10.0) → avg = 10.0
print(avg_gen.send(20.0))  # send(20.0) → avg = 15.0

gen = accumulate(5)
while True:
    try:
        print("Yielded:", next(gen))
    except StopIteration as e:
        print("Final result:", e.value)  # <-- captures the return value
        break




