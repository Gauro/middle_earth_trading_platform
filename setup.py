import os

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

# Get the directory of setup.py
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to req.txt
requirements_file = os.path.join(base_dir, "requirements.txt")

with open(requirements_file, "r") as fh:
    requirements = fh.read().splitlines()

setup(
    name="middle_earth_trading_platform",
    version="0.1.0",
    author="Gaurav Ail",
    author_email="ail.gaurav10@gmail.com",
    description="A Python module for trading weapons in the market of Bree",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    package_data={'middle_earth_trading_platform': ['data/config.ini']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
