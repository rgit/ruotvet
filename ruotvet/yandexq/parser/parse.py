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
    def prepare_question(text: str) -> str:
        output = []
        for word in text.split():
            prepared_word = ""
            for char in word:
                if char not in string.punctuation:
                    prepared_word += char
            if prepared_word != "":
                output.append(prepared_word)
        return " ".join(output).capitalize()

    @staticmethod
    def prepare_answer(text: str) -> str:
        output = []
        for word in text.rstrip(" ").rstrip("\n").split():
            output.append(word)
        return " ".join(output).capitalize()

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
