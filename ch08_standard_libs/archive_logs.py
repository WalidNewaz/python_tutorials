import os
import gzip
import shutil
from datetime import datetime
from pathlib import Path


def compress_file(source_path: Path, dest_path: Path):
    """Compress a log file using gzip."""
    with open(source_path, 'rb') as f_in:
        with gzip.open(dest_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def archive_logs(log_dir: str = "logs", archive_root: str = "archive"):
    log_dir_path = Path(log_dir)
    archive_root_path = Path(archive_root)

    if not log_dir_path.exists() or not log_dir_path.is_dir():
        print(f"Log directory '{log_dir}' not found.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_dir = archive_root_path / f"logs_{timestamp}"
    archive_dir.mkdir(parents=True, exist_ok=True)

    log_files = list(log_dir_path.glob("*.log"))
    if not log_files:
        print("No .log files found.")
        return

    for log_file in log_files:
        compressed_file = archive_dir / f"{log_file.stem}.log.gz"
        compress_file(log_file, compressed_file)
        print(f"Archived: {log_file} → {compressed_file}")

    print(f"All logs archived to: {archive_dir}")


if __name__ == "__main__":
    archive_logs()