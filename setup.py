from setuptools import find_packages, setup

setup(
    name="finance-tracker",
    version="2.0.0",
    author="Ahmad Akram",
    author_email="ahmadd.akram@example.com",
    description="Personal finance CLI — track income, expenses & savings from your terminal.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Ahmad-Akram7/FINANCE-TRACKER",
    packages=find_packages(exclude=["tests*", "legacy*"]),
    python_requires=">=3.9",
    install_requires=[
        "click>=8.1",
        "sqlalchemy>=2.0",
        "pydantic>=2.0",
        "rich>=13.0",
    ],
    extras_require={
        "charts": ["matplotlib>=3.7"],
        "dev":    ["pytest", "pytest-cov", "black", "ruff"],
    },
    entry_points={
        "console_scripts": [
            "finance-tracker=finance_tracker.interfaces.cli:cli",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Office/Business :: Financial",
    ],
)
