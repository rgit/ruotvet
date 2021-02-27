from ..http import AIOHTTPClient
from typing import Optional
from json import loads


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
        url = f"https://cse.google.com/cse/element/v1?rsz=filtered_cse&num={count}&hl={language_code}&source=gcsc" \
              f"&gss=.com&cselibv=323d4b81541ddb5b&cx=b9d53d8616ca5d2ae&q={query}1&safe=off" \
              f"&cse_tok=AJvRUv1Q-D5PxjpehBSJ6EnQP5hN:1614378606318&sort=&exp=csqr,cc&oq={query}" \
              "&gs_l=partner-generic.12...0.0.2.766337.0.0.0.0.0.0.0.0..0.0.csems%2Cnrl%3D13...0.0....34.partner-" \
              "generic..47.0.0.nm6aVyIGCn4&callback=google.search.cse.api3374"
        try:
            response = await self.client.request_text("GET", url, proxy=proxy)
            if "cursor" in response:
                response = response.split("google.search.cse.api3374(")[1][:-2]
                return loads(response)
        finally:
            await self.client.close()
