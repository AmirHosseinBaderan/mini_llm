import time
import requests

from storage.cache import FileCache


class HttpClient:

    def __init__(self):

        self.cache = FileCache()

    def get(self, url):

        cached = self.cache.get(url)

        if cached:
            return cached

        retries = 3

        for attempt in range(retries):

            try:

                response = requests.get(
                    url,
                    timeout=30
                )

                response.raise_for_status()

                data = response.json()

                self.cache.set(
                    url,
                    data
                )

                time.sleep(0.5)

                return data

            except Exception:

                if attempt == retries - 1:
                    raise

                time.sleep(2)