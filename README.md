# Openlibrary API

Runs on Python 3.8.

Install with pip: `pip install -r requirements.txt`

Make sure to set and export the DATABASE_URL environment variable before proceeding.

Run with `uvicorn src.app:app`
Run tests with `python -m pytest`. To run integration tests as well: `INTEGRATION_TEST=true python -m pytest`
Linting: `black src/ tests/`
