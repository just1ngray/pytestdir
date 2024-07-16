import json
from pathlib import Path

from .example import save_state_as_json


def test_save_state_as_json(pytestdir: Path):
    save_state_as_json(1, "one", pytestdir / "first.json")
    save_state_as_json(2, "two", pytestdir / "second.json")
    save_state_as_json(3, "three", pytestdir / "third.json")

    jsons = list(pytestdir.iterdir())
    assert len(jsons) == 3
    for json_path in jsons:
        with json_path.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert "version" in data
            assert "state" in data
