from requests.exceptions import InvalidSchema, InvalidURL
from .exceptions import InvalidRequestUrlException
import requests


class Request(requests.Request):
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }

    def make(self, method: str, url: str, body: dict = None, params: str = None, stream: bool = False):
        try:
            response = requests.request(
                method=method,
                url=url,
                data=body,
                params=params,
                headers=self.headers,
                allow_redirects=False,
                timeout=5,
                stream=stream
            )
        except (InvalidSchema, InvalidURL):
            raise InvalidRequestUrlException(
                "Requests.api raise an error: Invalid url or schema."
            )
        return response
