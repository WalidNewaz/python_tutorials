import csv

data = [["Name", "Age"], ["Alice", 30], ["Bob", 25]]

print("Working with CSV file")
print("======================")

# Write CSV file
with open("people.csv", "w") as file:
    print("Writing CSV file")
    writer = csv.writer(file)
    writer.writerows(data)

# Read CSV file
with open("people.csv", "r") as file:
    print("Reading CSV file")
    reader = csv.reader(file)
    for row in reader:
        print(row)