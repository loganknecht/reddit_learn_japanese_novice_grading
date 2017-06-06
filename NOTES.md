# General
Think silly bear, think.

# Questions
## How do you want the data ingested?
- Single file
    - per user
- Formatting
    - Questions are mapped to their number

## How do you want the data output?
Single files?

# Python Kakasi Model
## Kakasi Converter

## Fix hepburn pickle issue
1. Clone repo from here
    - https://github.com/miurahr/pykakasi
2. Change setup.py `_prebuild` references to `prebuild`
3. Go to root directory with venv active and perform
    1. python setup.py build
    2. python setup.py install
    3. python setup.py clean