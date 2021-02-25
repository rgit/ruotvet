from pydantic import BaseModel
from typing import List, Optional


class Attachment(BaseModel):
    """
    This object represents a question attachment, that contains the URL to the attachment,
    the path, where the file stored, and its title.
    """
    url: str
    path: Optional[str] = None
    title: Optional[str] = None


class Question(BaseModel):
    """
    This object represents a question, that contains the URL to the question,
    the question itself, the answer to this question, and attachments.
    """
    url: str
    question: Optional[str] = None
    answer: Optional[str] = None
    attachments: List[Optional[Attachment]] = None


class File(BaseModel):
    """
    This object represents a file. Contains a path and file format.
    """
    path: str
    format: str
