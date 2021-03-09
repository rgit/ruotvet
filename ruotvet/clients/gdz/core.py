from ruotvet.types import Question, Attachment
from ..exceptions import EmptyQueryError
from ruotvet.http import AIOHTTPClient
from typing import List, Optional
from ruotvet.utils import Google
import re


class GDZ:
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
                for url in response:
                    question = Question(url=url)
                    response_parsed = await self.parser.parse_question(await self.client.request_text(
                                                                       "GET", question.url, proxy=proxy))
                    output.append(question.copy(update=response_parsed))
                return output
            raise EmptyQueryError("The query must not be empty.")
        finally:
            await self.client.close()


class Parser:
    async def parse_question(self, response: str) -> Optional[dict]:
        question = re.findall(r'(?<=<h1 itemprop=\"name\">).*?(?:\<)', response)[0] or None
        images = re.findall(r'(?<=<img src="\/\/).{0,500}(?=" alt)', response)
        attachments = []
        for image in images:
            attachments.append(Attachment(url="https://" + image))
        return {"question": question, "answer": None, "attachments": attachments or None}
