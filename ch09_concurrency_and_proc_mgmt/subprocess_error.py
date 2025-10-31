import subprocess

try:
    subprocess.run(["ls", "nonexistent_folder"], check=True)
except subprocess.CalledProcessError as e:
    print("🛑 Failed:", e)