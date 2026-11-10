import csv
import io
import json

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from app.api.deps import CurrentUserDep, PostRepoDep, RedisDep, SessionDep
from app.db.database import async_session_maker
from app.db.models import Post, Tag, User, post_tags
from app.schemas.post import AuthorOut, AuthorStat, PostStat, PostOut, PostCreate, TagOut, TagStat

router = APIRouter(prefix="/posts")

POST_STATS_KEY = 'posts:stats'

@router.get('/native', response_model=list[PostOut])
async def list_posts_native(session: SessionDep, limit: int = Query(50, le=100)):
    # joinedload — автор подтягивается JOIN'ом в том же запросе (many-to-one),
    # selectinload — все теги одним доп. запросом WHERE post_id IN (...) (many-to-many)
    stmt = (
        select(Post)
        .options(joinedload(Post.author), selectinload(Post.tags))
        .order_by(Post.id)
        .limit(limit)
    )
    posts = (await session.scalars(stmt)).all()
    return [PostOut.model_validate(post) for post in posts]