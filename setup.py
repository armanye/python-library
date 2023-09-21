from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="python-library",
    version="0.1",
    packages=["python_library"],
    install_requires=requirements,
)
