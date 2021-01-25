from bs4 import BeautifulSoup
from requests import Response
import re


class Parser:
    @staticmethod
    def _regex_find(text: str):
        return re.findall(r"(<span>(.+?)</span>)", text)[0][1]

    def parse_search_results(self, response: Response):
        soup = BeautifulSoup(response.text, "html.parser")
        output = []
        for iteration in soup.find_all(href=True):
            if iteration:
                h3_element = iteration.findChildren("h3")
                if h3_element:
                    output.append([self._regex_find(str(h3_element[0])), iteration["href"]])
        return output
