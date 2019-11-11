import requests


def links_satis(url: str) -> requests.Response:
    return requests.get(url, stream=True)
