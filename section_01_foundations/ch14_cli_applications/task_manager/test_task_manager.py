import subprocess

def test_task_add_and_list():
    subprocess.run(["python", "main.py", "add", "--task", "Test CLI"], check=True)
    result = subprocess.run(["python", "main.py", "list"], capture_output=True, text=True)
    assert "Test CLI" in result.stdout