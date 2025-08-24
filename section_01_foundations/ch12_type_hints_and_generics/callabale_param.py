from typing import Callable


# --- Basic callable annotation --------------------------
def apply_twice(func: Callable[[int], int], x: int) -> int:
    """Apply a function to a value twice."""
    return func(func(x))

def square(x: int) -> int:
    return x ** 2

# --- Basic callable annotation --------------------------
def operate(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

def divide(a: int, b: int) -> float:
    return a / b

# --- Any parameter callable annotation --------------------------
def run_any(func: Callable[..., str]) -> str:
    """Callable with any number of arguments, but must return a string."""
    return func("Hello", "World")

def concatenate(a: str, b: str) -> str:
    return a + " " + b

# --- Strategy pattern --------------------------
class Calculator:
    def __init__(self, operation: Callable[[int, int], int]):
        self.operation = operation

    def compute(self, a: int, b: int) -> int:
        return self.operation(a, b)

# Different Strategies
add = lambda x, y: x + y
mul = lambda x, y: x * y

calc_add = Calculator(add)
calc_mul = Calculator(mul)

# --- Tests --------------------------------
print(apply_twice(square, 3))

print(operate(divide, 10, 2))

print(run_any(concatenate))

print(calc_add.compute(2, 3))  # 5
print(calc_mul.compute(2, 3))  # 6





