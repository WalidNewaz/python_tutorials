import json

data = { "name": "Alice", "skills": ["Python", "ML"] }

print("Working with JSON file")
print("======================")

# Write
with open("user.json", "w") as file:
    print("Writing JSON data to file")
    json.dump(data, file, indent=2)

# Read
with open("user.json", "r") as file:
    print ("Reading JSON file")
    print(json.load(file))