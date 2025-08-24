from pydantic import BaseModel, EmailStr, ValidationError
from typing import Optional

class UserModel(BaseModel):
    id: int
    name: str
    email: Optional[EmailStr] = None
    tags: list[str] = []

try:
    u = UserModel(id="1", name="Alice", email="@example.com", tags=("a", "b"))
    # id coerced to int; tags coerced to list
except ValidationError as e:
    print(e.json())
