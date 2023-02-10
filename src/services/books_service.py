import requests

class BooksService:

    endpoint = 'https://openlibrary.org/isbn/'

    def get(self, isbn):
        url = f'{self.endpoint}/{isbn}.json'
        response = requests.get(url)
        if response.status_code == 404:
            return {"status": "not found"}
        return response.json()
