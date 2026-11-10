from pydantic import BaseModel, ConfigDict, Field


class AuthorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str


class TagOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    author: AuthorOut
    tags: list[TagOut] = []


class PostCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    tags: list[str] = Field(default_factory=list, max_length=10)


class TagStat(BaseModel):
    id: int
    posts: int


class AuthorStat(BaseModel):
    username: str
    posts: int

class PostStat(BaseModel):
    total_posts: int
    avg_posts_per_author: float
    by_tag: list[TagStat]
    top_authors: list[AuthorOut]
    above_average: list[AuthorOut]

