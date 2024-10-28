from pathlib import Path

import pytest


_FOLDER_NAME = ".pytestdir"


@pytest.fixture
def pytestdir(request: pytest.FixtureRequest):
    """
    A simple fixture that creates a directory which is unique to the test function. When using this
    fixture, you shouldn't clean up files, as this is done automatically when running 'pytest' the
    next time.

    Remember that absolute paths will override pytestdir. E.g.,
    ```python
    def test_gotcha(pytestdir):
        path = pytestdir.joinpath("/etc/myprogram/configuration.ini")
        print(path.as_posix()) # /etc/myprogram/configuration.ini

        path = pytestdir.joinpath("etc/myprogram/configuration.ini")
        print(path.as_posix()) # /your/current/pwd/.pytestdir/etc/myprogram/configuration.ini
    ```
    """
    path = request.config.rootpath.joinpath(
        _FOLDER_NAME,
        request.node.path.relative_to(request.config.rootpath),
        request.node.name
    )

    try:
        path.mkdir(parents=True, exist_ok=False)
    except FileExistsError as exc:
        raise FileExistsError(f"Directory {path} already exists, but it should have been cleaned up "
                              f"by pytest_sessionstart!") from exc

    return path


def _rm_r(path: Path):
    """
    Basically the 'rm -r <path>' command, but in Python.
    """
    if not path.absolute():
        raise ValueError(f"Path {path} must be absolute to ensure safety!")

    if len(path.parts) < 2:
        raise ValueError(f"Refusing to remove path {path} because it's too high level!")

    if not path.is_dir():
        path.unlink()
        return

    for item in path.iterdir():
        _rm_r(item)

    path.rmdir()


def pytest_sessionstart(session: pytest.Session):
    """
    Cleanup from the previous session.
    """
    # remove previous test results
    pytestdir_folder = session.config.rootpath / _FOLDER_NAME
    if pytestdir_folder.exists():
        _rm_r(pytestdir_folder)

    # to avoid confusion look for other _FOLDER_NAME folders so they are removed as well
    for folder in session.config.rootpath.rglob(f"**/{_FOLDER_NAME}"):
        if not folder.is_dir():
            continue
        _rm_r(folder)


def pytest_collection_finish(session: pytest.Session):
    """
    If we've collected any tests using the pytestdir fixture, create a .gitignore so nothing
    gets accidentally committed.
    """
    pytestdir_used = False

    for item in session.items:
        if pytestdir.__name__ in item.fixturenames: # type: ignore
            pytestdir_used = True
            break

    if pytestdir_used:
        pytestdir_folder = session.config.rootpath / _FOLDER_NAME
        pytestdir_folder.mkdir()
        pytestdir_folder.joinpath(".gitignore").write_text("**")


def pytest_report_header(config: pytest.Config):
    """
    Prints the path to the pytestdir folder.
    """
    path = config.rootpath / _FOLDER_NAME
    print(f"pytestdir: {path.absolute().resolve()}")
