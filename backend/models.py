from pydantic import BaseModel
from typing import List


class Questionnaire(BaseModel):
    answers: List[int]

from typing import Dict

class ChatMessage(BaseModel):
    message: str
    scores: Dict
