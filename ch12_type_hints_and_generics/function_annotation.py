# You can annotate `parameters` and the `return types` of a function
from typing import Optional, Callable


def greet(name: str, age: int) -> str:
    return f"Hello, {name}! You are {age} years old."

def increment(x: int, step: int = 1) -> int:
    return x + step

def find_user(user_id: Optional[int]) -> str:
    if user_id is None:
        return "No user"
    return f"User {user_id}"

def apply_twice(func: Callable[[int], int], value: int) -> int:
    return func(func(value))

def double(value: int) -> int:
    return value * 2

# --- Tests --------------------------------

# Test function parameter annotation
print(greet("Alice", 22))      # Works
print(greet("Alice", "22"))    # IDE warning

# Test default parameter
print(increment(10))

# Test optional parameters
u_id = None
print(find_user(u_id))

# Test callable parameter annotation
print(apply_twice(double, 10))

