from pydantic import BaseModel
from typing import List, Optional


class Attachment(BaseModel):
    url: str
    save_path: str
    title: Optional[str]


class Question(BaseModel):
    url: str
    question: Optional[str]
    answer: Optional[str]
    attachments: List[Optional[Attachment]] = None
