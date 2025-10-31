# Variables can be annotated independently of assignment.
from typing import Optional
from dataclasses import dataclass


no_value: int
name: str = "Alice"
age: int = 30
scores: list[int] = [95, 88, 76]

class User:
    id: int
    name: str
    email: Optional[str] = None

    def __str__(self) -> str:
        return f"User(id={self.id}, name={self.name}, email={self.email or 'N/A'})"

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"

class Node:
    value: int
    next_node: "None | Node" = None # Quotes allow forward reference

    def __str__(self) -> str:
        return f"Node(value={self.value}, next_node={self.next_node})"

def add(x: int, y) -> int:
    return x + y

# --- Tests --------------------------------

# Test not initialized
no_value = 100
no_value = "100"

# Test class init
user_1 = User()
user_1.id = 100
user_1.name = "Alice"
print(user_1)
print(repr(user_1))

user_2 = User()
user_2.id = 200
user_2.name = "Bob"
user_2.email = "bob@email.com"
print(user_2)

# Test forward references
node_1 = Node()
node_1.value = 100

node_2 = Node()
node_2.value = 200
node_1.next_node = node_2
print(node_1)

# Test introspection
print(add.__annotations__)
print(user_1.__annotations__)
print(node_1.__annotations__)



