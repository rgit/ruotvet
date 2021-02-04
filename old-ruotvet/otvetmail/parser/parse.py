from dataclasses import dataclass
from bs4 import BeautifulSoup
from requests import Response
import typing


@dataclass
class Task:
    url: str
    question: str or None
    answer: str = None
    attachment: str = None


class Parser:
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

    def parse_question(self, response: Response) -> typing.List:
        soup = BeautifulSoup(response.text, "html.parser")
        question = soup.find("div", {"class": "q--qcomment medium"})
        answer = soup.find("div", {"class": "a--atext atext"})
        output = []

        if question is not None:
            output.append(self.prepare_answer(question.text))
        else:
            output.append("У вопроса нет заголовка.")
        if answer is not None:
            output.append(self.prepare_answer(answer.text))
        else:
            output.append("У вопроса нет текста ответа.")
        output.append(None)
        return output
