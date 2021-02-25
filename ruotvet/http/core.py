from abc import abstractmethod, ABC
import aiohttp
import asyncio


class AbstractHTTPClient(ABC):
    @abstractmethod
    async def request_text(self, method: str, url: str, body: dict = None, params: str = None,
                           proxy: str = None) -> str:
        ...

    @abstractmethod
    async def request_content(self, method: str, url: str, body: dict = None, params: str = None,
                              proxy: str = None) -> str:
        ...

    @abstractmethod
    async def request_json(self, method: str, url: str, body: dict = None, params: str = None,
                           proxy: str = None) -> str:
        ...

    @abstractmethod
    async def close(self):
        ...


class AIOHTTPClient:
    def __init__(self, session: aiohttp.ClientSession = None):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        self.session = session or aiohttp.ClientSession(
            loop=asyncio.get_event_loop(),
            connector=aiohttp.TCPConnector(ssl=False),
            trust_env=False
        )

    async def request_text(self, method: str, url: str, body: dict = None, params: dict = None,
                           proxy: str = None) -> str:
        """
        This function makes an async request to URL and returns text.
        :param method: Method for a request.
        :param url: Request URL.
        :param body: Request data.
        :param params: Query parameters.
        :param proxy: Proxy for request.
        :return: Request result.
        """
        async with self.session.request(
            method=method,
            url=url,
            data=body,
            params=params,
            headers=self.headers,
            allow_redirects=False,
            timeout=5,
            proxy=proxy
        ) as response:
            return await response.text()

    async def request_content(self, method: str, url: str, body: dict = None, params: dict = None,
                              proxy: str = None) -> bytes:
        """
        This function makes an async request to URL and returns bytes.
        :param method: Method for a request.
        :param url: Request URL.
        :param body: Request data.
        :param params: Query parameters.
        :param proxy: Proxy for request.
        :return: Request result.
        """
        async with self.session.request(
            method=method,
            url=url,
            data=body,
            params=params,
            headers=self.headers,
            allow_redirects=False,
            timeout=5,
            proxy=proxy
        ) as response:
            return await response.read()

    async def request_json(self, method: str, url: str, body: dict = None, params: dict = None,
                           proxy: str = None) -> dict:
        """
        This function makes an async request to URL and returns json.
        :param method: Method for a request.
        :param url: Request URL.
        :param body: Request data.
        :param params: Query parameters.
        :param proxy: Proxy for request.
        :return: Request result.
        """
        async with self.session.request(
            method=method,
            url=url,
            data=body,
            params=params,
            headers=self.headers,
            allow_redirects=False,
            timeout=5,
            proxy=proxy
        ) as response:
            return await response.json()

    async def close(self):
        """
        This function closes a session.
        """
        await self.session.close()
