from abc import ABC, abstractmethod
from dataclasses import dataclass

# Part interfaces
class Engine(ABC):
    @abstractmethod
    def spec(self) -> str:
        raise NotImplementedError("Subclasses must implement the 'spec' method.")

class Wheels(ABC):
    @abstractmethod
    def spec(self) -> str:
        raise NotImplementedError("Subclasses must implement the 'spec' method.")

class Infotainment(ABC):
    @abstractmethod
    def spec(self) -> str:
        raise NotImplementedError("Subclasses must implement the 'spec' method.")

# Tesla Model 3 parts
class Model3Engine(Engine):
    def spec(self) -> str:
        return "Dual-motor electric, 258 kW, 75 kWh pack"

class Model3Wheels(Wheels):
    def spec(self) -> str:
        return "19-inch aero wheels, EV-rated tires"

class Model3Infotainment(Infotainment):
    def spec(self) -> str:
        return "17-inch center screen, Tesla OS"

class Model3PerformanceWheels(Wheels):
    def spec(self) -> str:
        return "20-inch performance wheels, summer tires"

# Toyota Corolla parts
class CorollaEngine(Engine):
    def spec(self) -> str:
        return "1.8L I4 hybrid, 103 kW combined"

class CorollaWheels(Wheels):
    def spec(self) -> str:
        return "16-inch alloy wheels, all-season tires"

class CorollaInfotainment(Infotainment):
    def spec(self) -> str:
        return "8-inch touchscreen, Toyota Audio Multimedia"

class PartsFactory(ABC):
    @abstractmethod
    def create_engine(self) -> Engine:
        raise NotImplementedError("Subclasses must implement the 'create_engine' method.")
    @abstractmethod
    def create_wheels(self) -> Wheels:
        raise NotImplementedError("Subclasses must implement the 'create_wheels' method.")
    @abstractmethod
    def create_infotainment(self) -> Infotainment:
        raise NotImplementedError("Subclasses must implement the 'create_infotainment' method.")

class Model3Factory(PartsFactory):
    def create_engine(self) -> Engine:
        return Model3Engine()
    def create_wheels(self) -> Wheels:
        return Model3Wheels()
    def create_infotainment(self) -> Infotainment:
        return Model3Infotainment()

class CorollaFactory(PartsFactory):
    def create_engine(self) -> Engine:
        return CorollaEngine()
    def create_wheels(self) -> Wheels:
        return CorollaWheels()
    def create_infotainment(self) -> Infotainment:
        return CorollaInfotainment()

class Model3PerformanceFactory(Model3Factory):
    def create_wheels(self) -> Wheels:
        return Model3PerformanceWheels()  # engine & infotainment inherited

@dataclass
class Car:
    model: str
    engine: Engine
    wheels: Wheels
    infotainment: Infotainment

class CarAssembler:
    def __init__(self, factory: PartsFactory, model_name: str):
        self.factory = factory
        self.model_name = model_name

    def assemble(self) -> Car:
        engine = self.factory.create_engine()
        wheels = self.factory.create_wheels()
        infotainment = self.factory.create_infotainment()
        return Car(
            model=self.model_name,
            engine=engine,
            wheels=wheels,
            infotainment=infotainment,
        )

# Usage
car1 = CarAssembler(Model3Factory(), "Tesla Model 3").assemble()
car2 = CarAssembler(CorollaFactory(), "Toyota Corolla").assemble()
car3 = CarAssembler(Model3PerformanceFactory(), "Tesla Model 3 Performance").assemble()

print(car1.model, "|", car1.engine.spec(), "|", car1.wheels.spec(), "|", car1.infotainment.spec())
print(car2.model, "|", car2.engine.spec(), "|", car2.wheels.spec(), "|", car2.infotainment.spec())
print(car3.model, "|", car3.engine.spec(), "|", car3.wheels.spec(), "|", car3.infotainment.spec())
