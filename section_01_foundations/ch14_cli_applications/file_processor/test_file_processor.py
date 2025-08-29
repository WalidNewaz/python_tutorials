import subprocess

def test_file_processor_uppercase():
    subprocess.run(["python", "main.py", "input.txt", "output.txt","--strategy", "uppercase"], check=True)
    # result = subprocess.run(["python", "main.py", "list"], capture_output=True, text=True)
    # assert "Test CLI" in result.stdout
    input = ""
    output = ""
    with open("input.txt", 'r') as f:
        input = f.read()
    assert "this is an all lower case text." in input
    with open("output.txt", 'r') as f:
        output = f.read()
    assert "THIS IS AN ALL LOWER CASE TEXT." in output

def test_file_processor_reverse():
    subprocess.run(["python", "main.py", "input.txt", "output.txt","--strategy", "reverse"], check=True)
    # result = subprocess.run(["python", "main.py", "list"], capture_output=True, text=True)
    # assert "Test CLI" in result.stdout
    input = ""
    output = ""
    with open("input.txt", 'r') as f:
        input = f.read()
    assert "this is an all lower case text." in input
    with open("output.txt", 'r') as f:
        output = f.read()
    assert ".txet esac rewol lla na si siht" in output