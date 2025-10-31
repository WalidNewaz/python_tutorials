import argparse

parser = argparse.ArgumentParser(description="Simple CLI Calculator")
parser.add_argument("a", type=int, help="First number")
parser.add_argument("b", type=int, help="Second number")
parser.add_argument("--operation", choices=["add", "sub"], default="add")

args = parser.parse_args()

if args.operation == "add":
    print(args.a + args.b)
else:
    print(args.a - args.b)