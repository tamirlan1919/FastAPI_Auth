from pydantic import BaseModel
from datetime import datetime

class GithubUser(BaseModel):
    login: str
    name: str | None = None
    avatar_url: str
    html_url: str
    public_repos: int
    followers: int
    created_at: datetime
