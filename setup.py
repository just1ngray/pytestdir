from setuptools import setup

setup(
    name="pytestdir",
    version="0.1.0",
    packages=["pytestdir"],
    entry_points={ "pytest11": "name_of_plugin = pytestdir.plugin" },
    classifiers=["Framework :: Pytest"],
    install_requires=[
        "pytest>=7.0.0",
    ],
)
