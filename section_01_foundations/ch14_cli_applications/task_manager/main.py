import argparse
from commands.add import AddTaskCommand
from commands.list import ListTasksCommand

parser = argparse.ArgumentParser()
parser.add_argument("command", choices=["add", "list"])
parser.add_argument("--task", help="Task description (for add command)")

args = parser.parse_args()

if args.command == "add":
    cmd = AddTaskCommand(task=args.task)
elif args.command == "list":
    cmd = ListTasksCommand()

cmd.execute()