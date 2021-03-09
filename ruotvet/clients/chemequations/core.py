from ..exceptions import EmptyQueryError
from typing import Dict, Optional, List
from ruotvet.http import AIOHTTPClient
from ruotvet.types import Question
from bs4 import BeautifulSoup


class ChemEquations:
    def __init__(self):
        self.client = AIOHTTPClient()
        self.parser = Parser()

    async def get_answers(self, query: str, proxy: str = None) -> List[Question]:
        """
        This function makes a request for chemequations and gets an equation for substances.
        :param query: Search query.
        :param proxy: Proxy that will be used during request.
        :return: List of answered questions.
        """
        try:
            output = []
            if query:
                question = Question(url=f"https://chemequations.com/ru/?s={query.replace('+','+%2B+')}", question=query)
                response = await self.parser.parse_question(await self.client.request_text(
                    "GET", f"https://chemequations.com/ru/?s={query.replace('+', '+%2B+')}", proxy=proxy))
                output.append(question.copy(update=response))
                return output
            raise EmptyQueryError("The query must not be empty.")
        finally:
            await self.client.close()


class Parser:
    async def parse_question(self, response: str) -> Dict[str, Optional[str]]:
        soup = BeautifulSoup(response, "html.parser")
        multiple_solutions = soup.find("table", {"class": "table possible-solutions center"})
        if multiple_solutions:
            for url in [url.get("href") for url in multiple_solutions.find("tbody").find_all("a")]:
                response = await AIOHTTPClient().request_text("GET", f"https://chemequations.com/ru/{url}")
                soup = BeautifulSoup(response, "html.parser")
                answer = "".join([char.text.strip("\n").replace("\xa0", "").rstrip(" ") for char in
                                  soup.find_all("h1", {"class": "equation main-equation well"})])
                return {"answer": answer, "attachments": None}
        else:
            answer = "".join([char.text.strip("\n").replace("\xa0", "").rstrip(" ") for char in
                              soup.find_all("h1", {"class": "equation main-equation well"})])
            return {"answer": answer, "attachments": None}
