import threading
import time

# Constants
threads = []
files = [
    "https://www.google.com/",
    "https://www.youtube.com/",
    "https://www.mit.edu/"
]

def process(name):
    print(f"Processing {name}...")
    with open(f'resources/{name}.txt', 'r') as f:
        line = f.readline()
        # Print the first 30 characters
        # print(line[0:30])
        print(line)
        time.sleep(2)  # simulates file processing
    print(f"Done processing {name}")

def main():
    for i in range(1, 11):
        print(f"Starting thread {i}")
        process(f"file-{i}")

if __name__ == '__main__':
    main()