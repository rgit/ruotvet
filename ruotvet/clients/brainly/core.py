from ruotvet.types import Question, Attachment
from ..exceptions import EmptyQueryError
from ruotvet.http import AIOHTTPClient
from typing import List, Optional
from ruotvet.utils import Google
from bs4 import BeautifulSoup
import re


class Brainly:
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
                response = await Google().search(f"site:znanija.com {query}", count, proxy=proxy)
                if "results" in response:
                    for url in response["results"]:
                        question = Question(url=url["url"] + "/")
                        response = await self.parser.parse_question(await self.client.request_text(
                            "GET", question.url, proxy=proxy))
                        output.append(question.copy(update=response))
                return output
            raise EmptyQueryError("The query must not be empty.")
        finally:
            await self.client.close()


class Parser:
    @staticmethod
    def _match_media_url(text: str) -> str or None:
        try:
            return re.findall(r"(src=\"(.+?)\")", str(text))[0][1]
        except IndexError:
            return None

    @staticmethod
    def prepare_text(text: str) -> str:
        output = []
        for word in text.rstrip(" ").rstrip("\n").split():
            output.append(word)
        return " ".join(output).capitalize()

    async def parse_question(self, response: str) -> Optional[dict]:
        soup = BeautifulSoup(response, "html.parser")
        question = self.prepare_text(soup.find("h1", {"data-test": "question-box-text"}).text) or None
        answer = self.prepare_text(soup.find("div", {"data-test": "answer-box-text"}).text) or None
        attachment = self._match_media_url(soup.find("img", {"class": "brn-qpage-next-attachments-viewer-"
                                                                      "image-preview__image"}))
        if not attachment:
            attachment = self._match_media_url(soup.find("div", {"class": "sg-text sg-text--break-words brn-rich-"
                                                                          "content js-answer-content"}).find("img"))
        return {"question": question, "answer": answer, "attachments": [Attachment(url=attachment
                                                                                   )] if attachment else None}
