from ruotvet.types import Question, Attachment
from ..exceptions import EmptyQueryError
from ruotvet.http import AIOHTTPClient
from typing import List, Optional
from ruotvet.utils import Google
from bs4 import BeautifulSoup


class SuperResheba:
    def __init__(self):
        self.client = AIOHTTPClient()
        self.parser = Parser()

    async def get_answers(self, query: str, count: int = 1, proxy: str = None) -> List[Question]:
        """
        This function search for a query in google, after that parse results.
        :param query: Search query.
        :param count: Count of answers.
        :param proxy: Proxy that will be used during request.
        :return: List of answered questions.
        """
        try:
            if query:
                output = []
                response = await Google().search(f"site:gdz.ru {query}", count, proxy=proxy)
                if "results" in response:
                    for url in response["results"]:
                        question = Question(url=url["url"])
                        response = await self.parser.parse_question(await self.client.request_text(
                            "GET", question.url, proxy=proxy))
                        output.append(question.copy(update=response))
                return output
            raise EmptyQueryError("The query must not be empty.")
        finally:
            await self.client.close()


class Parser:
    @staticmethod
    def prepare_text(text: str) -> str:
        output = []
        for word in text.rstrip(" ").split():
            output.append(word)
        return " ".join(output).capitalize()

    async def parse_question(self, response: str) -> Optional[dict]:
        soup = BeautifulSoup(response, "html.parser")
        question = soup.find("div", {"class": "article_header"})
        question = self.prepare_text(question.text) if question else None
        answer = soup.find_all("div", {"class": "single-part"}) or None
        images = soup.find("div", {"itemprop": "acceptedAnswer"}) or None
        attachments = []
        if answer:
            text = ""
            for part in answer:
                text += part.text
            answer = self.prepare_text(text)
        if images:
            for image in images.find_all("img"):
                image_src = str(image).split("../../")[1].split("\" width")[0]
                attachments.append(Attachment(url=f"https://superresheba.by/{image_src}"))
        return {"question": question, "answer": answer, "attachments": attachments or None}
