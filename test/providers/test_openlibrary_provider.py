from unittest import mock


def test_search_passes_on_the_params_as_request_query_params_and_json_format(
    books_service, isbn
):
    with mock.patch("src.providers.openlibrary_provider.requests.get") as patched_get:
        mock_response = mock.MagicMock(status_code=200)
        patched_get.return_value = mock_response
        books_service.search({"isbn": isbn})
        patched_get.assert_called_once_with(
            mock.ANY, params={"isbn": isbn, "format": "json"}
        )


def test_search_unavailable(books_service, isbn):
    exception_thrown = False
    with mock.patch("src.providers.openlibrary_provider.requests.get") as patched_get:
        mock_response = mock.MagicMock(ok=False)
        patched_get.return_value = mock_response
        try:
            books_service.search({"isbn": isbn})
        except Exception:
            exception_thrown = True

    assert exception_thrown
