from client.request import Request
from .parser import Parser
from typing import List


class Google:
    def __init__(self):
        self.request = Request()

    def search_for_links(self, query: List[str], count: int = 10, offset: int = 0, language: str = "ru"):
        url = f"https://www.google.com/search?q={' '.join(query)}&start={offset}&num={count}&ie=utf-8&oe=utf-8" \
              f"&cr=countryRU&lr=lang_{language}"
        return Parser().parse_search_results(response=self.request.make("GET", url))

    # def search_in_presets(self, query: str):
    #     re.findall(r"znanija.com", "https://znanija.com/app/ask?entry=top&q=ТУТВОПРОС")

    def search_for_page(self, url: str):
        return self.request.make("GET", url)
