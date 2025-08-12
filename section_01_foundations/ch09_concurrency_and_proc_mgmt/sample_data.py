from pathlib import Path

Path("data").mkdir(exist_ok=True)

for i in range(5):
    with open(f"data/sample_{i}.log", 'w') as f:
        f.write("This is some text data.\n" * 1000)