from typing import Optional

from pydantic import BaseModel, Field


class TodoIn(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

class TodoOut(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None) # Маппинг _id на id
    title: str
    description: Optional[str] = None
    is_completed: bool = False

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None