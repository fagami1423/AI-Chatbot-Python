from urllib import response
from pydantic import BaseModel
from typing import List, Optional


class Question(BaseModel):
    tag: str
    patterns: List[str]
    responses: List[str]
    context_set: Optional [str]


