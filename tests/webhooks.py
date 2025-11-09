# tests/test_webhook_status_by_fixture.py
import json
import os
from pathlib import Path

import httpx
import pytest

TESTDATA_DIR = Path(__file__).parent.parent / "testdata"
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
ENDPOINT = "/webhook"


def collect_cases():
    cases = []
    if not TESTDATA_DIR.exists():
        return cases
    for status_dir in sorted(TESTDATA_DIR.iterdir()):
        if not status_dir.is_dir():
            continue
        try:
            expected = int(status_dir.name)
        except ValueError:
            continue
        for jf in sorted(status_dir.glob("*.json")):
            cases.append(pytest.param(jf, expected, id=f"{status_dir.name}/{jf.name}"))
    return cases


@pytest.mark.parametrize("json_path,expected_status", collect_cases())
def test_webhook_status(json_path: Path, expected_status: int):
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        r = client.post(ENDPOINT, json=payload, headers={"Accept": "application/json"})
    assert r.status_code == expected_status, (
        f"{json_path} -> {r.status_code} != {expected_status}"
    )
