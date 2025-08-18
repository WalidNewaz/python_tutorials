from abc import ABC, abstractmethod
import subprocess
from loguru import logger
from dataclasses import dataclass
import time
from typing import Optional
from pathlib import Path

@dataclass
class RunResult:
    exit_code: int
    stdout: str
    stderr: str
    image: str
    runtime_ms: int


class AbstractDockerRunner(ABC):
    @abstractmethod
    def run(self) -> RunResult:
        pass

class DockerCLI:
    def run(self, args, **kwargs) -> subprocess.CompletedProcess:
        return subprocess.run(args, **kwargs)

class PythonDockerRunner(AbstractDockerRunner):
    def __init__(
            self,
            script_file: str,
            *,
            image: str = "python:3.10-slim",
            cpus: str = "1",
            memory: str = "256m",
            network_none: bool = True,
            timeout_sec: Optional[int] = 30,
            user: Optional[str] = "65534:65534",  # non-root (nobody:nogroup) by default
            docker_cli = DockerCLI(),
            script_name_override: Optional[str] = None,
            workdir_in_container: str = "/work",
            readonly_mount: bool = True,
    ) -> None:
        self.script_path = Path(script_file).resolve()
        self.script_filename = "script.py"
        self.script_file = Path(script_file).resolve()  # Path to the script file
        self.image = image
        self.cpus = cpus
        self.memory = memory
        self.network_none = network_none
        self.timeout_sec = timeout_sec
        self.user = user
        self.docker_cli = docker_cli
        self.workdir = workdir_in_container
        self.readonly_mount = readonly_mount
        # If you want to force the name inside container (rare), pass override;
        # otherwise we use the actual filename of the provided script.
        self.script_name = script_name_override or self.script_path.name
        # host_dir is the parent of the script file (this answers your question).
        self.host_dir = str(self.script_path.parent)

    def run(self) -> RunResult:
        if not self.script_path.exists():
            msg = f"Script file not found: {self.script_path}"
            logger.error(msg)
            return RunResult(
                exit_code=127,
                stdout="",
                stderr=msg,
                image=self.image,
                runtime_ms=0,
            )

        mount_flag = f"{self.host_dir}:{self.workdir}"
        if self.readonly_mount:
            mount_flag += ":ro"

        cmd = [
            "docker", "run", "--rm",
            "-v", mount_flag,
            "-w", self.workdir,
            "--cpus", self.cpus,
            "--memory", self.memory,
        ]

        if self.network_none:
            cmd.extend(["--network", "none"])

        if self.user:
            cmd.extend(["--user", self.user])

        cmd.extend([self.image, "python", self.script_name])

        logger.info(
            "Running script in container",
            extra={"image": self.image, "workdir": self.workdir, "script": self.script_name}
        )

        start = time.perf_counter()
        try:
            # We do NOT set check=True because we want to capture stdout/stderr even on non-zero exit.
            proc = self.docker_cli.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout_sec,
            )
            elapsed_ms = int((time.perf_counter() - start) * 1000)

            if proc.returncode != 0:
                logger.warning(
                    "Container exited with non-zero code",
                    extra={"code": proc.returncode, "stderr": proc.stderr[:1000]}
                )

            return RunResult(
                exit_code=proc.returncode,
                stdout=proc.stdout,
                stderr=proc.stderr,
                image=self.image,
                runtime_ms=elapsed_ms,
            )

        except subprocess.TimeoutExpired as e:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            msg = f"Docker run timed out after {self.timeout_sec}s"
            logger.error(msg)
            return RunResult(
                exit_code=124,  # common timeout code
                stdout=e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or ""),
                stderr=(e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or "")) + f"\n{msg}",
                image=self.image,
                runtime_ms=elapsed_ms,
            )
        except FileNotFoundError:
            # docker CLI not found on host
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            msg = "Docker CLI not found. Is Docker installed and on PATH?"
            logger.error(msg)
            return RunResult(
                exit_code=127,
                stdout="",
                stderr=msg,
                image=self.image,
                runtime_ms=elapsed_ms,
            )
        except Exception as e:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            logger.exception("Unexpected error while running Docker")
            return RunResult(
                exit_code=1,
                stdout="",
                stderr=str(e),
                image=self.image,
                runtime_ms=elapsed_ms,
            )


class JavaScriptDockerRunner(AbstractDockerRunner):
    def __init__(
            self,
            script_file: str,
            docker_cli = DockerCLI(),
            *,
            image: str = "node:18-slim",
            cpus: str = "1",
            memory: str = "256m",
            network_none: bool = True,
            timeout_sec: Optional[int] = 30,
            user: Optional[str] = "65534:65534",  # non-root (nobody:nogroup) by default
            script_name_override: Optional[str] = None,
            workdir_in_container: str = "/work",
            readonly_mount: bool = True,
    ) -> None:
        self.script_path = Path(script_file).resolve()
        self.script_filename = "script.js"
        self.script_file = Path(script_file).resolve()  # Path to the script file
        self.image = image
        self.cpus = cpus
        self.memory = memory
        self.network_none = network_none
        self.timeout_sec = timeout_sec
        self.user = user
        self.docker_cli = docker_cli
        self.workdir = workdir_in_container
        self.readonly_mount = readonly_mount
        # If you want to force the name inside container (rare), pass override;
        # otherwise we use the actual filename of the provided script.
        self.script_name = script_name_override or self.script_path.name
        # host_dir is the parent of the script file (this answers your question).
        self.host_dir = str(self.script_path.parent)

    def run(self) -> RunResult:
        if not self.script_path.exists():
            msg = f"Script file not found: {self.script_path}"
            logger.error(msg)
            return RunResult(
                exit_code=127,
                stdout="",
                stderr=msg,
                image=self.image,
                runtime_ms=0,
            )

        mount_flag = f"{self.host_dir}:{self.workdir}"
        if self.readonly_mount:
            mount_flag += ":ro"

        cmd = [
            "docker", "run", "--rm",
            "-v", mount_flag,
            "-w", self.workdir,
            "--cpus", self.cpus,
            "--memory", self.memory,
        ]

        if self.network_none:
            cmd.extend(["--network", "none"])

        if self.user:
            cmd.extend(["--user", self.user])

        cmd.extend([self.image, "node", self.script_name])

        logger.info(
            "Running script in container",
            extra={"image": self.image, "workdir": self.workdir, "script": self.script_name}
        )

        start = time.perf_counter()
        try:
            # We do NOT set check=True because we want to capture stdout/stderr even on non-zero exit.
            proc = self.docker_cli.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout_sec,
            )
            elapsed_ms = int((time.perf_counter() - start) * 1000)

            if proc.returncode != 0:
                logger.warning(
                    "Container exited with non-zero code",
                    extra={"code": proc.returncode, "stderr": proc.stderr[:1000]}
                )

            return RunResult(
                exit_code=proc.returncode,
                stdout=proc.stdout,
                stderr=proc.stderr,
                image=self.image,
                runtime_ms=elapsed_ms,
            )

        except subprocess.TimeoutExpired as e:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            msg = f"Docker run timed out after {self.timeout_sec}s"
            logger.error(msg)
            return RunResult(
                exit_code=124,  # common timeout code
                stdout=e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or ""),
                stderr=(e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or "")) + f"\n{msg}",
                image=self.image,
                runtime_ms=elapsed_ms,
            )
        except FileNotFoundError:
            # docker CLI not found on host
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            msg = "Docker CLI not found. Is Docker installed and on PATH?"
            logger.error(msg)
            return RunResult(
                exit_code=127,
                stdout="",
                stderr=msg,
                image=self.image,
                runtime_ms=elapsed_ms,
            )
        except Exception as e:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            logger.exception("Unexpected error while running Docker")
            return RunResult(
                exit_code=1,
                stdout="",
                stderr=str(e),
                image=self.image,
                runtime_ms=elapsed_ms,
            )
