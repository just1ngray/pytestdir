from pathlib import Path
from typing import Literal

import pytest


def test_folder_exists(pytestdir: Path):
    assert pytestdir.exists()
    assert pytestdir.is_dir()

@pytest.mark.parametrize("test_param", [1, 2, 3])
def test_parametrize(test_param, pytestdir: Path):
    assert list(pytestdir.iterdir()) == []
    pytestdir.joinpath(f"file_{test_param}.txt").write_text(f"Hello, file #{test_param}!")

@pytest.mark.parametrize("a", [1])
@pytest.mark.parametrize("b", [1, 2])
@pytest.mark.parametrize("c", [1, 2, 3])
def test_multi_parametrize(a, b: Literal[1] | Literal[2], c, pytestdir: Path):
    assert list(pytestdir.iterdir()) == []
    pytestdir.joinpath("args.txt").write_text(f"a={a}, b={b}, c={c}")
