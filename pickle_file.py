import pickle

data = { "x": 1, "y": 2, "z": 3 }

print("Working with Pickle")
print("======================")

# Save binary
with open("pickle_data.pkl", "wb") as file:
    print("Writing to file")
    pickle.dump(data, file)

# Load binary file
with open("pickle_data.pkl", "rb") as file:
    print("Reading from file")
    restored_data = pickle.load(file)
    print(restored_data)


