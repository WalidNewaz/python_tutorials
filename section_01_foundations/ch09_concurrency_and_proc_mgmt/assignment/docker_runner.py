from abc import ABC, abstractmethod
import subprocess
import logging

# Application logger
logging.basicConfig(
    filename="docker_runner.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

class AbstractDockerRunner(ABC):
    @abstractmethod
    def run(self):
        pass

class PythonDockerRunner(AbstractDockerRunner):
    def __init__(self, script_file: str):
        self.script_filename = "script.py"
        self.script_file = script_file    # Path to the script file

    def run(self):
        try:
            # Launch a Docker container in detached mode
            container_name = "python_docker_subprocess"
            logging.info(f"Starting container {container_name}")
            subprocess.run(
                ["docker", "run", "-d", "--name", container_name, "python:3.10-slim", "sleep", "60"],
                check=True
            )
            # Copy Python file into container
            logging.info(f"Copying file {self.script_file} to container {container_name}")
            subprocess.run(
                ["docker", "cp", self.script_file, f"{container_name}:/{self.script_filename}"],
                check=True
            )
            # Run the Python program inside the container
            logging.info("Executing Python program inside container...")
            result = subprocess.run(
                ["docker", "exec", container_name, "python", self.script_filename],
                capture_output=True,
                text=True,
            )
            return result
        except ImportError:
            print(f"Failed to run Python code in container {container_name}")
            return None
        finally:
            # Stop the container
            logging.info(f"Stopping and removing container {container_name}...")
            subprocess.run(
                ["docker", "rm", "-f", container_name],
                check=True
            )


class JavaScriptDockerRunner(AbstractDockerRunner):
    def __init__(self, script_file: str):
        self.script_filename = "script.js"
        self.script_file = script_file  # Path to the script file

    def run(self):
        try:
            # Launch a Docker container in detached mode
            container_name = "javascript_docker_subprocess"
            logging.info(f"Starting container {container_name}")
            subprocess.run(
                ["docker", "run", "-d", "--name", container_name, "node:18-slim", "sleep", "60"],
                check=True
            )
            # Copy JavaScript file into container
            logging.info(f"Copying file {self.script_file} to container {container_name}")
            subprocess.run(
                ["docker", "cp", self.script_file, f"{container_name}:/{self.script_filename}"],
                check=True
            )
            # Run the JavaScript program inside the container
            logging.info("Executing JavaScript program inside container...")
            result = subprocess.run(
                ["docker", "exec", container_name, "node", self.script_filename],
                capture_output=True,
                text=True,
            )
            return result
        except FileNotFoundError:
            print(f"Failed to run Python code in container {container_name}")
            return None
        finally:
            # Step 6: Cleanup - Stop and remove the container
            logging.info(f"Stopping and removing container {container_name}...")
            subprocess.run(
                ["docker", "rm", "-f", container_name],
                check=True
            )
