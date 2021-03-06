from ..http import AIOHTTPClient
from typing import Optional
from json import loads
import re

class Google:
    def __init__(self):
        self.client = AIOHTTPClient()

    async def search(self, query: Optional[str], count: int = 1, language_code: str = "ru", proxy: str = None
                     ) -> Optional[dict]:
        """
        This function search for a query in google.
        :param query: Search query.
        :param count: Count of answers.
        :param language_code: Request language. By default, is Russian.
        :param proxy: Proxy that will be used during request.
        :return: List of answered questions.
        """
        escaped_search_term = query.replace(' ', '+')
        url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, 10,
                                                                              language_code)
        try:
            response = await self.client.request_text("GET", url, proxy=proxy)
            return re.findall(r'(?<=<a href=\"\/url\?esrc=s&amp;q=&amp;rct=j&amp;sa=U&amp;url=)(?:http).{0,500}?(?=\&amp)',str(response),re.MULTILINE)

        finally:
            await self.client.close()