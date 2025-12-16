from pydantic import BaseModel
from typing import Literal, Optional

# --- User & Auth Models ---

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Code Review Models ---

# MODIFICATION: Added "explain" to the list of allowed types
ReviewType = Literal["general", "documentation", "competitive", "refactor", "explain"]

class CodeReviewRequest(BaseModel):
    code: str
    review_type: ReviewType

class CodeReviewResponse(BaseModel):
    review_content: str

# --- Chat Models ---

class ChatRequest(BaseModel):
    message: str
    
class ChatResponse(BaseModel):
    reply: str