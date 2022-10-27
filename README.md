# CDX vs CDX

Compare two CycloneDX files and see which components each one have that the other does not have.

![screenshot of application](cdx-vs-cdx.png "Screenshot")

# How to run

## Option 1
### Currently only for Linux

Download the compressed file on the releases page, uncompress it and run the executable `cdx-vs-cdx`.

## Prerequisites for options 2 and 3

1. [Python](https://www.python.org/) 3.10
2. [Poetry](https://python-poetry.org/) 1.1

## Option 2

1. Clone this repository.
2. Install the dependencies with `poetry install`.
3. Run the program with `poetry run python main.py`

## Option 3

1. Clone this repository.
2. Install the dependencies with `poetry install`.
3. Compile the program with `pyinstaller main.py`.
4. Run the executable `main` inside `cdx-vs-cdx/dist/main`.