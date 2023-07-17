from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: Optional[str] = "bearer"


class TokenData(BaseModel):
    username: str
