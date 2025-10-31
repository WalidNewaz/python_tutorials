from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

# Part interfaces

@dataclass(frozen=True)
class Engine:
    name: str
    hp: int

@dataclass(frozen=True)
class Transmission:
    type: str  # "manual" | "automatic"

@dataclass(frozen=True)
class Tires:
    name: str
    rating: str  # "touring" | "sport"

@dataclass(frozen=True)
class Infotainment:
    screen_in: float
    supports_carplay: bool

# ----- Abstract Factory for parts -----
class PartsFactory(ABC):
    @abstractmethod
    def create_engine(self) -> Engine:
        raise NotImplementedError("Subclasses must implement the 'create_engine' method.")
    @abstractmethod
    def create_transmission(self) -> Transmission:
        raise NotImplementedError("Subclasses must implement the 'create_transmission' method.")
    @abstractmethod
    def create_tires(self) -> Tires:
        raise NotImplementedError("Subclasses must implement the 'create_tires' method.")

class EcoPartsFactory(PartsFactory):
    def create_engine(self) -> Engine:
        return Engine("I4 Hybrid", 180)
    def create_transmission(self) -> Transmission:
        return Transmission("automatic")
    def create_tires(self) -> Tires:
        return Tires("EcoGrip", "touring")

class PerformancePartsFactory(PartsFactory):
    def create_engine(self) -> Engine:
        return Engine("V8 Supercharged", 520)
    def create_transmission(self) -> Transmission:
        return Transmission("automatic")
    def create_tires(self) -> Tires:
        return Tires("TrackMax", "sport")

# ----- Abstract car -----
@dataclass(frozen=True)
class Car:
    model: str
    engine: Engine
    transmission: Transmission
    tires: Tires
    color: str
    infotainment: Optional[Infotainment] = None
    safety_pkg: Optional[str] = None  # "standard" | "advanced" | None

# ----- Car Builder -----
class CarBuilder:
    def __init__(self, model: str):
        self._model = model
        self._engine: Optional[Engine] = None
        self._transmission: Optional[Transmission] = None
        self._tires: Optional[Tires] = None
        self._color: Optional[str] = None
        self._infotainment: Optional[Infotainment] = None
        self._safety_pkg: Optional[str] = None

    # Fluent steps
    def with_engine(self, name: str, hp: int):
        self._engine = Engine(name, hp)
        return self

    def with_transmission(self, type_: str):
        self._transmission = Transmission(type_)
        return self

    def with_tires(self, name: str, rating: str):
        self._tires = Tires(name, rating)
        return self

    def painted(self, color: str):
        self._color = color
        return self

    def with_infotainment(self, screen_in: float, supports_carplay: bool = True):
        self._infotainment = Infotainment(screen_in, supports_carplay)
        return self

    def with_safety(self, pkg: str):
        self._safety_pkg = pkg
        return self

    # Validation lives here
    def _validate(self):
        if not all([self._engine, self._transmission, self._tires, self._color]):
            raise ValueError("Engine, transmission, tires, and color are required")

        # Example cross-part constraints:
        if self._engine.hp >= 350 and self._tires.rating != "sport":
            raise ValueError("High-HP build requires sport tires")

        if self._transmission.type == "manual" and self._engine.name == "EV":
            raise ValueError("Manual transmission not available for EV")

    def build(self) -> Car:
        self._validate()
        return Car(
            model=self._model,
            engine=self._engine,               # type: ignore[arg-type]
            transmission=self._transmission,   # type: ignore[arg-type]
            tires=self._tires,                 # type: ignore[arg-type]
            color=self._color,                 # type: ignore[arg-type]
            infotainment=self._infotainment,
            safety_pkg=self._safety_pkg,
        )

# ----- Builder that can accept factory-provided parts -----
class FactoryAwareCarBuilder(CarBuilder):
    def with_parts_from(self, factory: PartsFactory):
        self._engine = factory.create_engine()
        self._transmission = factory.create_transmission()
        self._tires = factory.create_tires()
        return self

eco_car = (
    FactoryAwareCarBuilder("Falcon E")
    .with_parts_from(EcoPartsFactory())
    .painted("Pearl White")
    .with_safety("standard")
    .build()
)
print(eco_car)

track_car = (
    FactoryAwareCarBuilder("Falcon R")
    .with_parts_from(PerformancePartsFactory())
    .painted("Racing Yellow")
    .with_infotainment(10.0)
    .with_safety("advanced")
    .build()
)
print(track_car)
