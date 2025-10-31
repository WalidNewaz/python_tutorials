# With **Generics**, you can write **functions and classes that work for all item types**,
# while keeping type safety.

from typing import TypeVar, TypedDict, Generic, Protocol, Literal, NewType
from pydantic import BaseModel
from dataclasses import dataclass

T = TypeVar('T')    # placeholder for any type

# Generic functions
def first(items: list[T]) -> T:
    """Return the first item in the list."""
    return items[0]

# Generic class
class Box(Generic[T]):
    """A generic container that holds one item of any type."""

    def __init__(self, item: T) -> None:
        self.item = item

    def get(self) -> T:
        return self.item

# Bounded variables
class Comparable(Protocol):
    def __lt__(self, other: object) -> bool: ...

U = TypeVar('U', bound=Comparable)

def minimum(a: U, b: U) -> U:
    return a if a < b else b

# Multiple TypeVars
K = TypeVar("K")
V = TypeVar("V")

def get_or_default(d: dict[K, V], key: K, default: V) -> V:
    return d.get(key, default)

# Aliases with Generics
Matrix = list[list[T]]

def transpose(matrix: Matrix[T]) -> Matrix[T]:
    return [list(row) for row in zip(*matrix)]

# Generics with Pydantic
class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: list[T]

class User(BaseModel):
    id: int
    name: str

# Protocols: Structural Subtyping
class Drivable(Protocol):
    def drive(self) -> None: ...

class Car:
    def drive(self) -> None: print("Car driving")

def start_journey(vehicle: Drivable):
    vehicle.drive()

# TypedDict: JSON-like schemas
class CarSpec(TypedDict):
    make: str
    model: str
    year: int
    electric: bool

# Literal: Restricted values
def paint(color: Literal["red", "blue"]):
    print("Paint color:", color)


type Mode = Literal['r', 'rb', 'w', 'wb']
def open_helper(file: str, mode: Mode) -> str: ...

# NewType: Strong semantic types
UserId = NewType('UserId', int)
Email = NewType('Email', str)

class CustomUser(BaseModel):
  id: UserId
  email: Email

  def __str__(self) -> str:
      return f"CustomUser(id={self.id}, email={self.email!r})"


# --- Tests --------------------------------
# Generic functions
print(first([1, 2, 3]))
print(first(["a", "b", "c"]))

# Generic class
int_box = Box(1)        # Box[int]
str_box = Box("hello")  # Box[str]
print(int_box.get())
print(str_box.get())

# Bounded variables
print(minimum(9, 7))
print(minimum("a", "b"))

# Multiple TypeVars
scores: dict[str, int] = {"alice": 90}
print(get_or_default(scores, "bob", 10))

# Aliases with Generics
print(transpose(transpose([[1, 2, 3], [4, 5, 6]])))

# Generics with Pydantic
resp = ApiResponse[User](success=True, data=[User(id=1, name="Alice"), User(id=2, name="Bob")])
print(resp.json())

# Protocols: Structural Subtyping
car = Car()
print(start_journey(car))

# TypedDict: JSON-like schemas
my_car: CarSpec = { "make": "For", "model": "Mustang", "year": 1967, "electric": False }
print(my_car)

# Literal: Restricted values
paint("red")
paint("orange")
open_helper('/other/path', 'typo')  # Error in type checker

# NewType: Strong semantic types
user = CustomUser(id=1, email="Alice")
print(user)
