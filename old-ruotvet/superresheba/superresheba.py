from ruotvet.utils import Request
from .parser import Parser, Task
from dataclasses import replace
import typing


class SuperResheba:
    def get_answers(self, query: str, count: int = 5, offset: int = 0, language: str = "ru") -> typing.List[Task]:
        request = Request()
        parser = Parser()
        output = []

        url = f"https://www.google.com/search?q=site:superresheba.by {query.lower()}&start={offset}&num={count}" \
              f"&ie=utf-8&oe=utf-8&lr=lang_{language}"

        answers = parser.parse_search_results(response=request.make("GET", url))

        for answer in answers:
            response = parser.parse_question(request.make("GET", answer.url))
            attachments = []
            for attachment in response[1]:
                attachments.append(self.get_attachment(attachment))
            output.append(replace(answer, **{"question": response[0], "attachments": attachments}))
        return output

    @staticmethod
    def get_attachment(url) -> str:
        request = Request()
        response = request.make("GET", url, stream=True)
        if response.status_code == 200:
            with open(f"media/{url.split('pic/')[1].split('/')[1]}", "+wb") as file:
                file.write(response.content)
                file.close()
            return f"media/{url.split('pic/')[1].split('/')[1]}"
