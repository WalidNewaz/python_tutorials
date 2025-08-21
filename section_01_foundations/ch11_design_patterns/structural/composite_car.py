from abc import ABC, abstractmethod
from typing import List

# ----- 1) Component -----
class CarComponent(ABC):
    @abstractmethod
    def total_cost(self) -> float: ...
    @abstractmethod
    def total_weight(self) -> float: ...
    @abstractmethod
    def describe(self, indent: int = 0) -> str: ...

# ----- 2) Leaf -----
class Part(CarComponent):
    def __init__(self, name: str, cost: float, weight: float):
        self.name = name
        self._cost = cost
        self._weight = weight

    def total_cost(self) -> float:
        return self._cost

    def total_weight(self) -> float:
        return self._weight

    def describe(self, indent: int = 0) -> str:
        pad = " " * indent
        return f"{pad}- Part: {self.name} | cost=${self._cost:.2f}, weight={self._weight:.1f}kg"

# ----- 3) Composite -----
class Assembly(CarComponent):
    def __init__(self, name: str):
        self.name = name
        self._children: List[CarComponent] = []

    def add(self, component: CarComponent) -> None:
        self._children.append(component)

    def remove(self, component: CarComponent) -> None:
        self._children.remove(component)

    def total_cost(self) -> float:
        return sum(c.total_cost() for c in self._children)

    def total_weight(self) -> float:
        return sum(c.total_weight() for c in self._children)

    def describe(self, indent: int = 0) -> str:
        pad = " " * indent
        lines = [f"{pad}+ Assembly: {self.name}"]
        for c in self._children:
            lines.append(c.describe(indent + 2))
        return "\n".join(lines)

# ---- Usage ---------------------------------------------------------
if __name__ == "__main__":
    # Leaves
    piston = Part("Piston", 40.0, 1.2)
    spark_plug = Part("Spark Plug", 8.0, 0.1)
    block = Part("Engine Block", 500.0, 90.0)
    wheel = Part("Wheel", 120.0, 12.0)

    # Sub-assemblies
    cylinder = Assembly("Cylinder")
    cylinder.add(piston)
    cylinder.add(spark_plug)

    engine = Assembly("Engine")
    engine.add(block)
    engine.add(cylinder)

    wheels = Assembly("Wheel Set")
    for _ in range(4):
        wheels.add(wheel)

    # Top-level assembly (car)
    car = Assembly("Car")
    car.add(engine)
    car.add(wheels)

    print(car.describe())
    print(f"\nTOTAL COST:  ${car.total_cost():.2f}")
    print(f"TOTAL WEIGHT: {car.total_weight():.1f} kg")