from pydantic import BaseModel
from typing import List, Optional


class File(BaseModel):
    """
    This object represents a file. Contains a path and file format.
    """
    filename: str
    path: str
    format: str


class Attachment(BaseModel):
    """
    This object represents a question attachment, that contains the URL to the attachment,
    the path, where the file stored, and its title.
    """
    url: str
    file: Optional[File] = None
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
