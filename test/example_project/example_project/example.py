from pathlib import Path


def save_state_as_json(version: int, state: str, target: Path):
    target.write_text(f'{{"version": {version}, "state": "{state}"}}')
