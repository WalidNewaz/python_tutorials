import yaml

data = {"server": {"port": 8080, "debug": True}}

print("Working with YAML file")

# Write YAML
with open("config.yaml", "w") as file:
    print("Writing to file")
    yaml.dump(data, file)

# Read YAML
with open("config.yaml", "r") as file:
    print("Reading from file")
    loaded = yaml.safe_load(file)
    print(loaded)