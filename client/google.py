from client.request import Request, InvalidRequestUrlException
from .parser import Parser
from typing import List
import re


class Google:
    def __init__(self):
        self.request = Request()

    def dirty_search(self, query: List[str], count: int = 5, offset: int = 0, language: str = "ru"):
        url = f"https://www.google.com/search?q=site:znanija.com{' '.join(query)}&start={offset}&num={count}&ie=utf-8" \
              f"&oe=utf-8&cr=countryRU&lr=lang_{language}"
        urls = Parser().parse_search_results(response=self.request.make("GET", url))
        output = []
        for url in urls:
            try:
                text = re.findall(r"(\w[а-яА-Я]+)", self.request.make("GET", url[1]).text)
            except InvalidRequestUrlException:
                continue
            if text:
                text = " ".join(Parser().prepare_text([pair.lower() for pair in text]))
                output.append(" ".join(text.split()[:20]).capitalize())
        return output

    def search(self, query: str):
        # re.findall(r"znanija.com", "https://znanija.com/app/ask?entry=top&q=ТУТВОПРОС")
        return self.request.make("GET", f"https://znanija.com/app/ask?entry=top&q={query}")
