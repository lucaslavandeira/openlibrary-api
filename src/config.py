import os

OPEN_LIBRARY_PROVIDER_ENDPOINT = os.getenv(
    "OPEN_LIBRARY_PROVIDER_ENDPOINT", "https://openlibrary.org/"
)

PAGINATION_DEFAULT_LIMIT = 10


DATABASE_URL = os.getenv("DATABASE_URL")
