from ruotvet.request import Request
from .parser import Parser, Task
from dataclasses import replace
import typing


class YandexQ:
    @staticmethod
    def get_answers(query: str, count: int = 5, offset: int = 0, language: str = "ru") -> typing.List[Task]:
        request = Request()
        parser = Parser()
        output = []

        url = f"https://www.google.com/search?q=site:yandex.ru/q/ {query.lower()}&start={offset}&num={count}" \
              f"&ie=utf-8&oe=utf-8&lr=lang_{language}"

        answers = parser.parse_search_results(response=request.make("GET", url))

        for answer in answers:
            url = f"https://yandex.ru/znatoki/web-api/aggregate/page/qQuestionRoute?eventName=qQuestionRoute&" \
                  f"id={answer.url.split('/')[-2]}&exp_flags=new_quality"

            response = request.make("GET", url).json()["entities"]

            question_text, answer_text = None, None

            for question_obj in response["question"]:
                question_title = response["question"][question_obj]["title"]
                question_text = response["question"][question_obj]["text"]
                if question_title is not None:
                    question_text = f"{question_title}\n{question_title}"
                else:
                    question_text = question_text
                break
            for answer_obj in response["answer"]:
                if response["answer"][answer_obj]["good"] is True:
                    answer_text = response["answer"][answer_obj]["plainText"]
                    if answer_text is not None:
                        answer_text = answer_text
                    break
            output.append(replace(answer, **{"question": question_text, "answer": answer_text}))
        return output
