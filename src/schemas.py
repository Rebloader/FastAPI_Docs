from datetime import datetime

from pydantic import BaseModel


class DocumentModel(BaseModel):
    id: int
    path: str
    date: datetime


class DocumentText(BaseModel):
    id_doc: int
    text: str
