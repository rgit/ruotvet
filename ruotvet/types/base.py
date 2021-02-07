from pydantic import BaseModel
from typing import List, Optional


class Attachment(BaseModel):
    url: str
    path: Optional[str] = None
    title: Optional[str] = None


class Question(BaseModel):
    url: str
    question: Optional[str] = None
    answer: Optional[str] = None
    attachments: List[Optional[Attachment]] = None
