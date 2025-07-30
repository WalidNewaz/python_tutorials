import json
from section_01_foundations.ch04_error_handling.log_parser import parse_log_file

def test_log_parser(tmp_path):
    log_file = tmp_path / "server.log"
    output_file = tmp_path / "server_log.json"

    log_file.write_text("[INFO] Test log\n[ERROR] Crash")

    results = parse_log_file(log_file, output_file)

    assert results[0]["level"] == "INFO"
    assert results[1]["message"] == "Crash"

    saved = json.loads(output_file.read_text())
    assert saved == results
