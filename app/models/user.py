from dataclasses import dataclass, field


@dataclass
class User:
    id: int
    username: str
    email: str
    hashed_password: str
    roles: list[str] = field(default_factory=list)



