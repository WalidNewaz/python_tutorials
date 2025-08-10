import subprocess

with open("output.txt", "w") as f:
    subprocess.run(["echo", "Hello subprocess!"], stdout=f)