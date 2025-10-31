from typing import Callable

# Simple example
UserId = int
Score = float

def record_score(user: UserId, score: Score) -> None:
    print(f"User {user} scored: {score}")


# Complex aliasing
Node = str
AdjList = dict[Node, set[Node]]

# Function type
Transform = Callable[[Node], Node]

def apply_pipeline(data: list[str], steps: list[Transform]) -> list[str]:
    for step in steps:
        data = [step(x) for x in data]
    return data


# --- Tests --------------------------------
record_score(101, 9.5)

my_steps: list[Transform] = [str.strip, str.upper]     # Applied str functions
print(apply_pipeline(["hello", "world"], my_steps))