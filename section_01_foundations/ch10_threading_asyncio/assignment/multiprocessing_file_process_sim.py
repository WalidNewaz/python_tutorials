from multiprocessing import Pool
from pathlib import Path
import time

def process(name):
    print(f"Processing {name}...")
    time.sleep(2)  # simulates file processing
    print(f"Done processing {name}")

async def main():
    pass

if __name__ == '__main__':
    main()
