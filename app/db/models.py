from datetime import datetime

from sqlalchemy import JSON, String, ForeignKey, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import select

from app.db.database import Base


post_tags = Table(
    'post_tags',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id', ondelete='CASCADE'),primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
)

class User(Base):
    __tablename__ = 'users'


    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    roles: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

    profile: Mapped["Profile | None"] = relationship(
        "Profile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    #Уровень БД реальный столбец
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    #Увроень Python posts.author - объект User
    #Этого столбца в таблице не будет

    author: Mapped["User"] = relationship(back_populates="posts")

    tags: Mapped[list["Tag"]] = relationship(secondary=post_tags, back_populates="posts")


class Profile(Base):
    __tablename__ = 'profiles'

    id: Mapped[int] = mapped_column(primary_key=True)
    bio: Mapped[str]
    city: Mapped[str]
    country: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True) #Unique - True связь будет 1 к 1

    user: Mapped["User"] = relationship("User", back_populates="profile")


class Tag(Base):
    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)

    posts: Mapped[list["Post"]] = relationship(secondary=post_tags, back_populates="tags")


class Test(Base):
    __tablename__ = 'tests'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)