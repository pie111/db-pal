# setup.py
from setuptools import setup, find_packages

setup(
    name="db-agent",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "argparse",
        # Add your other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "dbagent=db_agent.__main__:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A CLI tool for database interactions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/db-agent",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)