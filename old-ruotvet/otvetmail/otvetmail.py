from ruotvet.utils import Request
from .parser import Parser, Task
from dataclasses import replace
import typing


class OtvetMail:
    @staticmethod
    def get_answers(query: str, count: int = 5, offset: int = 0, language: str = "ru") -> typing.List[Task]:
        request = Request()
        parser = Parser()
        output = []

        url = f"https://www.google.com/search?q=site:otvet.mail.ru {query.lower()}&start={offset}&num={count}" \
              f"&ie=utf-8&oe=utf-8&lr=lang_{language}"

        answers = parser.parse_search_results(response=request.make("GET", url))
        for answer in answers:
            question_text, answer_text, attachment = parser.parse_question(request.make("GET", answer.url))
            output.append(replace(answer, **{"question": question_text, "answer": answer_text,
                                             "attachment": attachment}))
        return output
