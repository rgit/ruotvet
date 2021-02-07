from ruotvet.http import AIOHTTPClient
from ruotvet.types import Question, Attachment
from typing import List, Optional


class MailRu:
    def __init__(self):
        self.client = AIOHTTPClient()

    async def get_answers(self, query: str, count: int = 1) -> List[Optional[Question]]:
        output = []
        try:
            response = await self.client.request_json("GET", "https://otvet.mail.ru/go-proxy/answer_json",
                                                      params={"ajax_id": "0", "q": query, "num": count})
            for result in response["results"]:
                response = await self.client.request_json("POST", "https://otvet.mail.ru/api/",
                                                          body={"qid": result["id"], "__urlp": "/v2/question?ajax_id=0",
                                                                "sort": "1"})
                for answer in response["answers"]:
                    if "canth_status" in answer:
                        if answer["canth_status"] == 1:
                            attachment = [Attachment(url=answer["src"])] if "src" in answer else None
                            output.append(Question(url=result["url"], question=response["qtext"],
                                                   answer=answer["atext"], attachments=attachment))
                            break
            return output
        finally:
            await self.client.close()
