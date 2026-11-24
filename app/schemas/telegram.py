from pydantic import BaseModel

class TelegramLinkOut(BaseModel):
    url: str
    expires_in: int