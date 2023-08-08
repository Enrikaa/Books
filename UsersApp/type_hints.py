from typing import TypedDict


class UserCreationDict(TypedDict):
    username: str
    email: str
    is_administrator: bool
