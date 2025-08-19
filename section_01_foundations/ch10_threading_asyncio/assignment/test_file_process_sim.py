# test_file_process_sim.py
import asyncio
import anyio
import re
from pathlib import Path
import types
import time as _time

import pytest

# Change this to your module name/path if different
import file_process_sim as m


@pytest.fixture
def test_files(tmp_path: Path):
    """
    Create a few small text files with a mix of empty and non-empty lines.
    Return both the file paths (as strings) and the expected totals.
    """
    contents = [
        "hello\n\nworld\n",         # 2 non-empty lines, 5 + 5 = 10 chars
        "a\nbcd\n   \n",            # 2 non-empty, 1 + 3 = 4 chars
        "X\nY\nZ\n\n",              # 3 non-empty, 1 + 1 + 1 = 3 chars
    ]
    files = []
    total_lines = 0
    total_chars = 0

    res_dir = tmp_path / "resources"
    res_dir.mkdir()

    for i, text in enumerate(contents, start=1):
        p = res_dir / f"file-{i}.txt"
        p.write_text(text, encoding="utf-8")
        files.append(str(p))

        # mirror the program logic: count non-empty lines after strip()
        for line in text.splitlines():
            pl = line.strip()
            if pl:
                total_lines += 1
                total_chars += len(pl)

    return files, total_lines, total_chars


@pytest.fixture(autouse=True)
def fast_sleep(monkeypatch):
    """
    Speed up tests by removing real sleeps for sequential and threaded paths.
    We DO NOT monkeypatch time.sleep globally—only the module under test.
    """
    monkeypatch.setattr(m.time, "sleep", lambda _secs: None)


@pytest.mark.skip(reason="This test is temporarily disabled")
async def test_process_files_async(test_files, monkeypatch):
    files, exp_lines, exp_chars = test_files

    # Make asyncio.sleep yield without waiting
    async def _fast_async_sleep(_secs):
        await anyio.sleep(0)  # yield to event loop immediately

    monkeypatch.setattr(m.asyncio, "sleep", _fast_async_sleep)

    dur, total_lines, total_chars = await m.process_files_async(files)
    assert total_lines == exp_lines
    assert total_chars == exp_chars
    # duration string sanity check: "x.xx s"
    assert re.match(r"^\d+\.\d{2} s$", dur)


def test_process_files_seq(test_files):
    files, exp_lines, exp_chars = test_files
    dur, total_lines, total_chars = m.process_files_seq(files)
    assert total_lines == exp_lines
    assert total_chars == exp_chars
    assert re.match(r"^\d+\.\d{2} s$", dur)


def test_process_files_threaded(test_files):
    files, exp_lines, exp_chars = test_files

    # Ensure the global queue is empty before starting
    while not m.q.empty():
        _ = m.q.get_nowait()

    dur, total_lines, total_chars = m.process_files_threaded(files)
    assert total_lines == exp_lines
    assert total_chars == exp_chars
    assert re.match(r"^\d+\.\d{2} s$", dur)

    # Queue should be empty after aggregation
    assert m.q.qsize() == 0


@pytest.mark.skip(reason="This test is temporarily disabled")
def test_process_files_multiprocessing_small(test_files):
    """
    Keep multiprocessing workload small to avoid long CI runs.
    Note: monkeypatching time.sleep does NOT affect child processes,
    so this test runs "for real"—use a subset of files.
    """
    files, exp_lines, exp_chars = test_files

    small = files[:1]  # single file to keep it fast (~2s in original code)
    # Recompute the expected for the subset
    with open(small[0], "r", encoding="utf-8") as f:
        lines = 0
        chars = 0
        for line in f:
            pl = line.strip()
            if pl:
                lines += 1
                chars += len(pl)

    dur, total_lines, total_chars = m.process_files_multiprocessing(small)
    assert total_lines == lines
    assert total_chars == chars
    assert re.match(r"^\d+\.\d{2} s$", dur)
