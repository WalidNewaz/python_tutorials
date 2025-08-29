
import argparse
from strategies import UppercaseStrategy, ReverseStrategy

strategies = {
    "uppercase": UppercaseStrategy,
    "reverse": ReverseStrategy
}

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
parser.add_argument("--strategy", choices=strategies.keys(), required=True)

args = parser.parse_args()

with open(args.input, 'r') as f:
    data = f.read()

strategy = strategies[args.strategy]()
result = strategy.process(data)

with open(args.output, 'w') as f:
    f.write(result)

print(f"File processed using {args.strategy}.")