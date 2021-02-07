from ruotvet.http import AIOHTTPClient
from ruotvet.types import Question, Attachment
from bs4 import BeautifulSoup
from typing import List, Optional, AsyncGenerator
import re


class Znanija:
    def __init__(self):
        self.client = AIOHTTPClient()
        self.parser = Parser()

    async def get_answers(self, query: str, count: int = 1) -> List[Question]:
        url = f"https://www.google.com/search?q=site:znanija.com {query.lower()}&start=0&num={count + 1}" \
              f"&ie=utf-8&oe=utf-8&lr=lang_ru"
        output = []
        try:
            async for question in self.parser.parse_search_results(await self.client.request_text("GET", url)):
                response = await self.parser.parse_question(await self.client.request_text("GET", question.url))
                output.append(question.copy(update=response))
            return output
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

    @staticmethod
    async def parse_search_results(response: str) -> AsyncGenerator[Optional[Question], None]:
        soup = BeautifulSoup(response, "html.parser")
        for iteration in soup.find_all(href=True):
            if iteration and iteration.findChildren("h3"):
                if iteration["href"].startswith("https"):
                    yield Question(url=iteration["href"])

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
                                                                                   ) if attachment else None]}
