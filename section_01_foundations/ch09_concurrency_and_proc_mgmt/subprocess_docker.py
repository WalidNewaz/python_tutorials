import subprocess
import os
import tempfile
import textwrap
import logging

logging.basicConfig(
    filename="docker_runner.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Step 1: Define the Python code to be run inside the container
logging.info("Define the Python code to be run inside the container")
python_code = textwrap.dedent("""
print("Hello from inside Docker!")
for i in range(5):
    print(f"Processing item {i + 1}")                              
""")
python_code_filename = "app.py"

# Step 2: Create a temporary Python file
temp_dir = tempfile.mkdtemp()
python_file_path = os.path.join(temp_dir, python_code_filename)

with open(python_file_path, "w") as f:
    f.write(python_code)

logging.info(f"Created Python file at {python_file_path}")

# Step 3: Launch a Docker container in detached mode
container_name = "python_docker_subprocess"

logging.info(f"Starting container {container_name}")
subprocess.run(
    ["docker", "run", "-d", "--name", container_name, "python:3.10-slim", "sleep", "60"],
    check=True
)

# Step 4: Copy Python file into container
logging.info(f"Copying file {python_file_path} to container {container_name}")
subprocess.run(
    ["docker", "cp", python_file_path, f"{container_name}:/{python_code_filename}"],
    check=True
)

# Step 5: Run the Python program inside the container
logging.info("Executing Python program inside container...")
result = subprocess.run(
    ["docker", "exec", container_name, "python", python_code_filename],
    capture_output=True,
    text=True,
)

print("[INFO] Output from container:\n", result.stdout)
logging.info(f"Output from container: {result.stdout}")

# Step 6: Cleanup - Stop and remove the container
logging.info(f"Stopping and removing container {container_name}...")
subprocess.run(
    ["docker", "rm", "-f", container_name],
    check=True
)

# Step 7: Remove the temporary file
os.remove(python_file_path)
os.rmdir(temp_dir)
logging.info("Cleanup complete")
