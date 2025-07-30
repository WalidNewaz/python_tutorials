import os
import json
import sys


def parse_log_file(input_path, output_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError("Log file not found!")

    entries = []
    with open(input_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("[") and "]" in line:
                level_end = line.index("]")
                level = line[1:level_end]
                message = line[level_end + 1:].strip()
                entries.append({"level": level, "message": message})

    with open(output_path, "w") as file:
        json.dump(entries, file, indent=4)

    return entries

if __name__ == "__main__":
    parse_log_file(sys.argv[1], sys.argv[2])