import sys
import types
from pathlib import Path

# -------------------------------------------------------------------
# Ensure tests don't break if loguru isn't installed in the environment
# -------------------------------------------------------------------
try:
    from loguru import logger
except ModuleNotFoundError:
    fake_logger = types.SimpleNamespace(
        info=lambda *a, **k: None,
        warning=lambda *a, **k: None,
        error=lambda *a, **k: None,
        exception=lambda *a, **k: None,
    )
    sys.modules["loguru"] = types.SimpleNamespace(logger=fake_logger)
    from loguru import logger  # now safe to import

# rest of your imports
import subprocess
import pytest
from docker_runner import (
    RunResult,
    PythonDockerRunner,
    JavaScriptDockerRunner,
    DockerCLI,
)
from docker_runner import (
    PythonDockerRunner,
    JavaScriptDockerRunner,
    RunResult,
)

# ---------- Test doubles ----------

# Create a dummy logger if loguru is missing
if "loguru" not in sys.modules:
    fake_logger = types.SimpleNamespace(
        info=lambda *a, **k: None,
        warning=lambda *a, **k: None,
        error=lambda *a, **k: None,
        exception=lambda *a, **k: None,
    )
    sys.modules["loguru"] = types.SimpleNamespace(logger=fake_logger)

class StubCLI:
    """
    A tiny stub around subprocess.run to:
      - simulate success / failure / timeout
      - record last command called
      - avoid needing Docker
    """
    def __init__(
        self,
        *,
        returncode: int = 0,
        stdout: str = "OK",
        stderr: str = "",
        raise_exc: Exception | None = None,
    ) -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.raise_exc = raise_exc
        self.calls: list[list[str]] = []  # capture argv lists

    def run(self, args, **kwargs) -> subprocess.CompletedProcess:
        # Record the args used to call docker
        self.calls.append(list(args))

        # Raise exception if configured (e.g., TimeoutExpired, FileNotFoundError)
        if self.raise_exc is not None:
            raise self.raise_exc

        # Return a fabricated CompletedProcess
        return subprocess.CompletedProcess(
            args=args,
            returncode=self.returncode,
            stdout=self.stdout,
            stderr=self.stderr
        )

# ---------- Fixtures ----------

@pytest.fixture
def tmp_python_script(tmp_path: Path) -> Path:
    p = tmp_path / "hello.py"
    p.write_text('print("hello from python")\n')
    return p

@pytest.fixture
def tmp_js_script(tmp_path: Path) -> Path:
    p = tmp_path / "hello.js"
    p.write_text('console.log("hello from js")\n')
    return p

# ---------- PythonDockerRunner tests ----------

def test_python_runner_success_builds_expected_command(tmp_python_script: Path):
    cli = StubCLI(stdout="hello from python\n", returncode=0)
    runner = PythonDockerRunner(
        script_file=str(tmp_python_script),
        docker_cli=cli,
        image="python:3.10-slim",
        cpus=1,
        memory="128m",
        network_none=True,
        user="65534:65534",
        workdir_in_container="/work",
        readonly_mount=True,
    )

    result = runner.run()

    # 1) Result shaped correctly
    assert isinstance(result, RunResult)
    assert result.exit_code == 0
    assert "hello from python" in result.stdout
    assert result.image == "python:3.10-slim"
    assert result.runtime_ms >= 0

    # 2) Only one docker invocation for this design
    assert len(cli.calls) == 1

    cmd = cli.calls[0]
    # Base structure
    assert cmd[:3] == ["docker", "run", "--rm"]
    # Volume mount (read-only)
    assert "-v" in cmd
    mount_index = cmd.index("-v") + 1
    assert cmd[mount_index].endswith(":/work:ro")
    # Workdir
    assert "-w" in cmd and cmd[cmd.index("-w") + 1] == "/work"
    # Memory
    assert "--memory" in cmd and cmd[cmd.index("--memory") + 1] == "128m"
    # CPUs flag present because cpus=1
    assert "--cpus" in cmd and cmd[cmd.index("--cpus") + 1] == "1"
    # Network none flag present
    assert "--network" in cmd and cmd[cmd.index("--network") + 1] == "none"
    # User flag present
    assert "--user" in cmd and cmd[cmd.index("--user") + 1] == "65534:65534"
    # Image + interpreter + script name at end
    assert cmd[-3:] == ["python:3.10-slim", "python", tmp_python_script.name]

def test_python_runner_omits_cpus_when_invalid(tmp_python_script: Path):
    # cpus=0 should be considered invalid by your validation; flag not added
    cli = StubCLI(stdout="ok")
    runner = PythonDockerRunner(
        script_file=str(tmp_python_script),
        docker_cli=cli,
        cpus=0,  # invalid by your guard
    )
    _ = runner.run()
    cmd = cli.calls[0]
    assert "--cpus" not in cmd  # guard worked

@pytest.mark.parametrize("network_none", [True, False])
def test_python_runner_network_flag_toggles(tmp_python_script: Path, network_none: bool):
    cli = StubCLI(stdout="ok")
    runner = PythonDockerRunner(
        script_file=str(tmp_python_script),
        docker_cli=cli,
        network_none=network_none,
    )
    _ = runner.run()
    cmd = cli.calls[0]
    if network_none:
        assert "--network" in cmd and cmd[cmd.index("--network") + 1] == "none"
    else:
        assert "--network" not in cmd

def test_python_runner_adds_platform_when_provided(tmp_python_script: Path):
    cli = StubCLI(stdout="ok")
    runner = PythonDockerRunner(
        script_file=str(tmp_python_script),
        docker_cli=cli,
        container_platform="linux/amd64",
    )
    _ = runner.run()
    cmd = cli.calls[0]
    assert "--platform" in cmd
    assert cmd[cmd.index("--platform") + 1] == "linux/amd64"

def test_python_runner_missing_script_returns_127(tmp_path: Path):
    missing = tmp_path / "does_not_exist.py"
    cli = StubCLI(stdout="won't be used")
    runner = PythonDockerRunner(script_file=str(missing), docker_cli=cli)
    result = runner.run()

    assert result.exit_code == 127
    assert "not found" in result.stderr.lower()
    # Should not have called docker at all
    assert cli.calls == []

def test_python_runner_nonzero_exit_is_returned(tmp_python_script: Path):
    cli = StubCLI(returncode=2, stdout="", stderr="Traceback...")
    runner = PythonDockerRunner(script_file=str(tmp_python_script), docker_cli=cli)
    result = runner.run()
    assert result.exit_code == 2
    assert "Traceback" in result.stderr

def test_python_runner_timeout_is_mapped_to_124(tmp_python_script: Path):
    exc = subprocess.TimeoutExpired(
        cmd=["docker", "run"],
        timeout=1,
        output="partial out",
        stderr="partial err",
    )
    cli = StubCLI(raise_exc=exc)
    runner = PythonDockerRunner(
        script_file=str(tmp_python_script),
        docker_cli=cli,
        timeout_sec=1,
    )
    result = runner.run()
    assert result.exit_code == 124
    assert "timed out" in result.stderr.lower()
    # stdout from exception should be captured
    assert "partial out" in result.stdout

def test_python_runner_docker_cli_missing_maps_to_127(tmp_python_script: Path):
    cli = StubCLI(raise_exc=FileNotFoundError("docker not on PATH"))
    runner = PythonDockerRunner(script_file=str(tmp_python_script), docker_cli=cli)
    result = runner.run()
    assert result.exit_code == 127
    assert "docker cli not found" in result.stderr.lower()

def test_python_runner_unexpected_exception_maps_to_1(tmp_python_script: Path):
    cli = StubCLI(raise_exc=RuntimeError("boom"))
    runner = PythonDockerRunner(script_file=str(tmp_python_script), docker_cli=cli)
    result = runner.run()
    assert result.exit_code == 1
    assert "boom" in result.stderr

def test_python_runner_to_dict_roundtrip(tmp_python_script: Path):
    cli = StubCLI(stdout="ok")
    runner = PythonDockerRunner(script_file=str(tmp_python_script), docker_cli=cli)
    result = runner.run()
    d = result.to_dict()
    assert d["exit_code"] == result.exit_code
    assert d["stdout"] == result.stdout
    assert d["stderr"] == result.stderr
    assert d["image"] == result.image
    assert d["runtime_ms"] == result.runtime_ms

# ---------- JavaScriptDockerRunner smoke tests ----------

def test_js_runner_success_builds_expected_command(tmp_js_script: Path):
    cli = StubCLI(stdout='hello from js\n', returncode=0)
    runner = JavaScriptDockerRunner(
        script_file=str(tmp_js_script),
        docker_cli=cli,
        image="node:18-slim",
        memory="64m",
        network_none=False,  # ensure flag is omitted
        user=None,           # ensure flag is omitted
        readonly_mount=False # ensure :ro is omitted
    )
    result = runner.run()
    assert result.exit_code == 0
    cmd = cli.calls[0]
    assert cmd[:3] == ["docker", "run", "--rm"]
    # Volume mount read-write
    assert "-v" in cmd
    mount = cmd[cmd.index("-v")+1]
    assert mount.endswith(":/work")           # no :ro
    # No network none
    assert "--network" not in cmd
    # No user flag
    assert "--user" not in cmd
    # tail includes image + node + script
    assert cmd[-3:] == ["node:18-slim", "node", tmp_js_script.name]

def test_js_runner_missing_script_returns_127(tmp_path: Path):
    missing = tmp_path / "nope.js"
    cli = StubCLI(stdout="unused")
    runner = JavaScriptDockerRunner(script_file=str(missing), docker_cli=cli)
    result = runner.run()
    assert result.exit_code == 127
    assert cli.calls == []




