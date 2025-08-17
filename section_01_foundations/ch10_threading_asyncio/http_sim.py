import asyncio

async def fetch(name):
    print(f"Fetching {name}...")
    await asyncio.sleep(2)  # simulates network I/O
    print(f"Done fetching {name}")

async def main():
    await asyncio.gather(fetch("page1"), fetch("page2"), fetch("page3"))

asyncio.run(main())