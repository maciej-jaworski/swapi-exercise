from typing import Optional

import requests
from django.conf import settings


class StarWarsAPIClient:
    def __init__(self, session: Optional[requests.Session] = None):
        self.session = session or requests.Session()

    def get_full_list_of(self, what: str):
        url_to_fetch = f"{settings.STAR_WARS_API_HOST}/api/{what}/"
        results = []

        while url_to_fetch:
            response = self.session.get(url_to_fetch)
            response.raise_for_status()
            response_contents = response.json()

            results += response_contents["results"]
            url_to_fetch = response_contents["next"]

        return results


class RelatedResourceAttributeRetriever:
    """
    Retrieve specified attribute of remote JSON endpoint
    Cache result on instance
    """

    def __init__(self, attribute_to_retrieve: str, session: Optional[requests.Session] = None):
        self.session = session or requests.Session()
        self.cache = {}
        self.attribute_to_retrieve = attribute_to_retrieve

    def fetch_from_url(self, url: str):
        if url not in self.cache:
            response = self.session.get(url)
            response.raise_for_status()
            self.cache[url] = response.json()[self.attribute_to_retrieve]

        return self.cache[url]
