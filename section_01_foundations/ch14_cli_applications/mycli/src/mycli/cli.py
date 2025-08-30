import sys
from .commands import InitCommand, RunCommand, DeployCommand

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

    cmd = cmd_class()
    cmd.execute()