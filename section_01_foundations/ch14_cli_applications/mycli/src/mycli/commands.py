from abc import ABC, abstractmethod

# --- Command interface --------------------------------
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

# --- Concrete commands --------------------------------
class InitCommand(Command):
    def execute(self) -> None:
        print("Project initialized!")

class RunCommand(Command):
    def execute(self) -> None:
        print("Running project...")

class DeployCommand(Command):
    def execute(self) -> None:
        print("Deploying project...")