from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "Hotel Reservation Prediction",
    version = "0.0.1",
    author = "Owais Bin Mushtaq",
    packages=find_packages(),
    install_requires = requirements,
)