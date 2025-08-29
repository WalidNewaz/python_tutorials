from abc import ABC, abstractmethod
import sys

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

# --- Decorators ---------------------------------------
class LoggingDecorator(Command):
    def __init__(self, command: Command):
        self._command = command

    def execute(self):
        print(f"[LOG] Executing {self._command.__class__.__name__}")
        self._command.execute()
        print(f"[LOG] Finished {self._command.__class__.__name__}")

# Command registry (Invoker)
COMMANDS = {
    "init": InitCommand,
    "run": RunCommand,
    "deploy": DeployCommand
}

def main():
    if len(sys.argv) < 2:
        print("Usage: {} [init|run|deploy]".format(sys.argv[0]))
        return

    command = sys.argv[1]
    cmd_class = COMMANDS.get(command)
    if cmd_class is None:
        print("Usage: {} [init|run|deploy]".format(sys.argv[0]))
        return

    cmd = LoggingDecorator(cmd_class())
    cmd.execute()


if __name__ == "__main__":
    main()