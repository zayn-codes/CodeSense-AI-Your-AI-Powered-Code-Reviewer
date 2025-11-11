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

ReviewType = Literal["general", "documentation", "competitive"]

class CodeReviewRequest(BaseModel):
    code: str
    review_type: ReviewType

class CodeReviewResponse(BaseModel):
    review_type: ReviewType
    review_content: str

# --- Chat Models ---

class ChatRequest(BaseModel):
    message: str
    # We could add chat_history here later
    
class ChatResponse(BaseModel):
    reply: str