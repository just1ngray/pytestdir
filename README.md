# pytestdir

Pytest, and Python more generally, already have systems in place to work with
temporary files and directories. But for various reasons, they can be
inconvienient to work with.

- Python's `tempfile` should be used within a context to ensure clean-up, but
  increases indentation and clutters the test
- Pytest's `tmpdir` fixture yields an unfamiliar object of type `py.path.local`
- Pytest's `tmp_path` must be created before it can be used
- Temporary resources are created elsewhere on disk unless `--basetemp` is
  provided as a pytest argument

## Installation

One day this might be packaged on pypi.

```shell
pip install git+https://github.com/just1ngray/pytestdir.git
```

## About

`pytestdir` is a fixture that creates a `.gitignore`'d directory in your pytest
root where each test can receive a distinct and unique folder. The created
`.pytestdir/` folder will be deleted *next* time you run `pytest`, which allows
you to manually inspect the contents/results from the test.

```python
def test_serialization(pytestdir: Path):
    myobj = ...
    serialized = myobj.yaml()
    pytestdir.joinpath("serialized.yaml").write_text(serialized, "utf-8")

    assert ...
```

This has proven rather useful for:

- Inspecting in more detail the results of a test, as this can often provide
  more information and context than assertions or logs
- Setting up a test without relying so heavily on mocks, especially when
  implementations can change and then break your mocked setup
- Aiding other fixtures for state information: save logs, download database
  contents, save images, etc.

```python
@pytest.fixture
def mydb(pytestdir: Path):
    with DB() as db:
        # before the test
        db.clear()

        # give the test a reference to the db object, for setup + running + asserting
        yield db

        # teardown & save db results
        db.save_to(pytestdir / "db")
        db.clear()
```
