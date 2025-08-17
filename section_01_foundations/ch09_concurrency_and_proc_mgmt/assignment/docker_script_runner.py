from docker_runner import *
import os
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

logging.info("Define the JavaScript code to be run inside the container")
javascript_code = textwrap.dedent("""
console.log("Hello from inside Docker!")
for (let i = 0; i < 5; i++){
    console.log(`Processing item ${i + 1}`)
}
""")
js_code_filename = "app.js"

if __name__ == "__main__":
    # Python: Create a temporary Python file
    temp_dir = tempfile.mkdtemp()
    python_file_path = os.path.join(temp_dir, python_code_filename)
    code_runner = PythonDockerRunner(python_code, python_code_filename, temp_dir)
    # Run the container and save the result
    py_result = code_runner.run()
    print("[INFO] Output from Py container:\n", py_result.stdout)
    logging.info(f"Output from Py container: {py_result.stdout}")

    # JavaScript: Create the temporary JavaScript file
    js_temp_dir = tempfile.mkdtemp()
    js_file_path = os.path.join(js_temp_dir, js_code_filename)
    js_runner = JavaScriptDockerRunner(javascript_code, js_code_filename, js_temp_dir)
    # Run the container and save the result
    js_result = js_runner.run()
    print("[INFO] Output from JS container:\n", js_result.stdout)
    logging.info(f"Output from JS container: {js_result.stdout}")
