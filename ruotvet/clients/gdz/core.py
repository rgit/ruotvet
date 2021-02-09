from typing import List, Optional, AsyncGenerator
from ruotvet.types import Question, Attachment
from ..exceptions import EmptyQueryError
from ruotvet.http import AIOHTTPClient
from bs4 import BeautifulSoup
import re


class GDZ:
    def __init__(self):
        self.client = AIOHTTPClient()
        self.parser = Parser()

    async def get_answers(self, query: str, count: int = 1) -> List[Question]:
        """
        This function search for a query in google, after that parse results.
        :param query: Search query.
        :param count: Count of answers.
        :return: List of answered questions.
        """
        try:
            if query:
                url = f"https://www.google.com/search?q=site:gdz.ru {query.lower()}&start=0&num={count}" \
                      f"&ie=utf-8&oe=utf-8&lr=lang_ru"
                output = []
                async for question in self.parser.parse_search_results(await self.client.request_text("GET", url)):
                    response = await self.parser.parse_question(await self.client.request_text("GET", question.url))
                    output.append(question.copy(update=response))
                return output
            raise EmptyQueryError("The query must not be empty.")
        finally:
            await self.client.close()


class Parser:
    @staticmethod
    def _match_media_url(text: str) -> str or None:
        try:
            src = "https://" + re.findall(r"(src=\"//(.+?)\")", str(text))[0][1]
            if "&amp;" in src:
                return src.replace("&amp;", "&")
            return src
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
        question = self.prepare_text(soup.find("h1", {"itemprop": "name"}).text or None)
        images = soup.find_all("div", {"class": "task-img-container"})
        attachments = []
        for image in images:
            if image.find("img"):
                attachments.append(Attachment(url=self._match_media_url(image.find("img"))))
        return {"question": question, "answer": None, "attachments": attachments or None}
