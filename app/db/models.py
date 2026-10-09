from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column


from app.db.database import Base


class User(Base):
    __tablename__ = 'user'


    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    roles: Mapped[list[str]] = mapped_column(JSON, default=list)
