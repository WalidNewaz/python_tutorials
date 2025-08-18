import os
import tempfile
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from docker_runner import *
from logging_config import *
from loguru import logger

# Load environment variables from the .env file (if present)
load_dotenv()

# Application Constants
SCRIPTS_DIR = os.getenv('SCRIPTS_DIR')
LOGS_DIR = os.getenv('LOGS_DIR')
python_code_filename = "app.py"
js_code_filename = "app.js"


def run_script(script_type, script_src) -> str :
    """
    Instantiates and invokes the correct code runner based on the script type.
    :param script_type:
    :param script_src:
    :return:
    """
    # Create the temporary file
    temp_dir = tempfile.mkdtemp()
    temp_filepath: str = ""
    runner: Optional[AbstractDockerRunner] = None
    if script_type == "python":
        temp_filepath = os.path.join(temp_dir, python_code_filename)
        with open(temp_filepath, "w") as f:
            f.write(script_src)
        logger.info(f"Created {script_type} file at {temp_filepath}")
        runner = PythonDockerRunner(temp_filepath)
    elif script_type == "javascript":
        temp_filepath = os.path.join(temp_dir, js_code_filename)
        with open(temp_filepath, "w") as f:
            f.write(script_src)
        logger.info(f"Created {script_type} file at {temp_filepath}")
        runner = JavaScriptDockerRunner(temp_filepath)

    # Run the container and save the result
    result = runner.run()
    # Remove the temporary file
    os.remove(temp_filepath)
    os.rmdir(temp_dir)
    logger.info("Cleanup complete")
    return result.stdout

def get_script_type(file_path):
    """
    Reads the file path suffix and determines whether it is a JavaScript file
    or a Python script
    :param file_path:
    :return:
    """
    if file_path.suffix == ".py":
        return "python"
    elif file_path.suffix == ".js":
        return "javascript"
    else:
        return None

def main():
    """
    Executes all the scripts in the scripts directory.
    :return:
    """
    scripts_dir_path = Path(SCRIPTS_DIR)

    if not scripts_dir_path.exists() or not scripts_dir_path.is_dir():
        print(f"Scripts directory '{scripts_dir_path}' not found.")
        return

    script_files = [
        p.resolve()
            for p in scripts_dir_path.glob("**/*")
            if p.suffix in {".js", ".py"}
    ]
    if not script_files:
        print("No script files found.")
        return

    for script_file in script_files:
        with open(script_file, "r") as f_in:
            content = f_in.read()
            script_type = get_script_type(script_file)
            print(f"Executing {script_type}:\n--------------------------\n{content}")
            result = run_script(script_type, content)
            print("[INFO] Output from JS container:\n", result)
            logger.info(f"Output from JS container: {result}")


if __name__ == "__main__":
    main()

