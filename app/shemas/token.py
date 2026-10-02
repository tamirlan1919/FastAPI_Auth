from pydantic import BaseModel
from typing import List


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenPayload(BaseModel):
    sub: str | None = None
    roles : List[str] = []