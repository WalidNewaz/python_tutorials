from abc import ABC, abstractmethod
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


class AbstractDockerRunner(ABC):
    @abstractmethod
    def run(self):
        pass


class PythonDockerRunner(AbstractDockerRunner):
    def __init__(self, python_code, python_code_filename, temp_dir):
        self.python_code = python_code
        self.python_code_filename = python_code_filename
        self.temp_dir = temp_dir

    def run(self):
        try:
            python_file_path = os.path.join(self.temp_dir, self.python_code_filename)
            with open(python_file_path, "w") as f:
                f.write(self.python_code)
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
                ["docker", "cp", python_file_path, f"{container_name}:/{self.python_code_filename}"],
                check=True
            )
            # Step 5: Run the Python program inside the container
            logging.info("Executing Python program inside container...")
            result = subprocess.run(
                ["docker", "exec", container_name, "python", self.python_code_filename],
                capture_output=True,
                text=True,
            )
            # # Step 6: Cleanup - Stop and remove the container
            # logging.info(f"Stopping and removing container {container_name}...")
            # subprocess.run(
            #     ["docker", "rm", "-f", container_name],
            #     check=True
            # )
            # # Step 7: Remove the temporary file
            # os.remove(python_file_path)
            # os.rmdir(self.temp_dir)
            # logging.info("Cleanup complete")
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
            # Step 7: Remove the temporary file
            os.remove(python_file_path)
            os.rmdir(self.temp_dir)
            logging.info("Cleanup complete")


class JavaScriptDockerRunner(AbstractDockerRunner):
    def __init__(self, javascript_code, javascript_code_filename, temp_dir):
        self.javascript_code = javascript_code
        self.javascript_code_filename = javascript_code_filename
        self.temp_dir = temp_dir

    def run(self):
        try:
            javascript_file_path = os.path.join(self.temp_dir, self.javascript_code_filename)
            with open(javascript_file_path, "w") as f:
                f.write(self.javascript_code)
            logging.info(f"Created JavaScript file at {javascript_file_path}")

            # Step 3: Launch a Docker container in detached mode
            container_name = "javascript_docker_subprocess"
            logging.info(f"Starting container {container_name}")
            subprocess.run(
                ["docker", "run", "-d", "--name", container_name, "node:18-slim", "sleep", "60"],
                check=True
            )
            # Step 4: Copy JavaScript file into container
            logging.info(f"Copying file {javascript_file_path} to container {container_name}")
            subprocess.run(
                ["docker", "cp", javascript_file_path, f"{container_name}:/{self.javascript_code_filename}"],
                check=True
            )
            # Step 5: Run the JavaScript program inside the container
            logging.info("Executing JavaScript program inside container...")
            result = subprocess.run(
                ["docker", "exec", container_name, "node", self.javascript_code_filename],
                capture_output=True,
                text=True,
            )
            # # Step 6: Cleanup - Stop and remove the container
            # logging.info(f"Stopping and removing container {container_name}...")
            # subprocess.run(
            #     ["docker", "rm", "-f", container_name],
            #     check=True
            # )
            # # Step 7: Remove the temporary file
            # os.remove(javascript_file_path)
            # os.rmdir(self.temp_dir)
            # logging.info("Cleanup complete")
            return result
        except FileNotFoundError:
            print(f"Failed to find JavaScript file at {javascript_file_path}")
            return None
        finally:
            # Step 6: Cleanup - Stop and remove the container
            logging.info(f"Stopping and removing container {container_name}...")
            subprocess.run(
                ["docker", "rm", "-f", container_name],
                check=True
            )
            # Step 7: Remove the temporary file
            os.remove(javascript_file_path)
            os.rmdir(self.temp_dir)
            logging.info("Cleanup complete")
