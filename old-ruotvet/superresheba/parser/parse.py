from dataclasses import dataclass
from bs4 import BeautifulSoup
from requests import Response
import typing


@dataclass
class Task:
    url: str
    question: str or None
    attachments: list = None


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
        output = []

        question = soup.find("div", {"class": "article_header"}).text

        if question:
            output.append(" ".join(question.split()))

        images = soup.find("div", {"itemprop": "acceptedAnswer"}).find_all("img")

        if images:
            images_output = []
            for image in images:
                image_src = str(image).split("../../")[1].split("\" width")[0]
                images_output.append(f"https://superresheba.by/{image_src}")
            if images_output:
                output.append(images_output)
        return output
