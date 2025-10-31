import subprocess

from Cython.Build.Tests.TestIpythonMagic import capture_output

# Run a command and capture its output
result = subprocess.run(['ls','-la'], capture_output=True, text=True)

print("Exit Code:", result.returncode)
print("Output:", result.stdout)