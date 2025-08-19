import asyncio
import time


async def process(name):
    print(f"Processing {name}...")
    await asyncio.sleep(2)  # simulates file processing
    print(f"Done processing {name}")

async def main():
    pass

if __name__ == '__main__':
    main()