from dataclasses import dataclass
from bs4 import BeautifulSoup
from requests import Response
import typing
import string
import re


@dataclass
class Task:
    url: str
    question: str or None
    answer: str = None
    attachment: str = None


class Parser:
    @staticmethod
    def parse_search_results(response: Response) -> typing.List[Task]:
        soup = BeautifulSoup(response.text, "html.parser")
        output = []
        for iteration in soup.find_all(href=True):
            if iteration:
                h3_element = iteration.findChildren("h3")
                if h3_element:
                    if iteration["href"].startswith("https"):
                        output.append(
                            Task(url=iteration["href"], question=None)
                        )
        return output
