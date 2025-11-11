import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

# Import from our other backend files
import database
import models
import gemini_client
from models import User, UserCreate, CodeReviewRequest, CodeReviewResponse, ChatRequest, ChatResponse, Token

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Generate a secret key with: openssl rand -hex 32
SECRET_KEY = os.getenv("SECRET_KEY", "a_very_insecure_default_key_replace_me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- App & DB Initialization ---
app = FastAPI(title="AI Code Reviewer API")
database.init_db()  # Create database and tables on startup
gemini_client.configure_gemini() # Configure Gemini API on startup

# --- CORS ---
# This allows our Streamlit app (from a different URL) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to your Streamlit app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Security & Auth ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Creates a new JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """Decodes token and returns the current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = models.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user_data = database.get_user(username=token_data.username)
    if user_data is None:
        raise credentials_exception
    
    # Convert the sqlite3.Row object to our Pydantic User model
    user = User(id=user_data['id'], username=user_data['username'])
    return user

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "AI Code Reviewer API is running."}

@app.post("/register", response_model=User)
async def register_user(user: UserCreate):
    """Registers a new user."""
    db_user = database.get_user(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = database.create_user(username=user.username, password=user.password)
    if not new_user:
        raise HTTPException(status_code=500, detail="Could not create user")
        
    return User(id=new_user['id'], username=new_user['username'])

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Provides a JWT token for a valid username and password."""
    user = database.get_user(form_data.username)
    if not user or not database.verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    """Returns the current authenticated user's details."""
    return current_user

@app.post("/review", response_model=CodeReviewResponse)
async def get_review(
    request: CodeReviewRequest,
    current_user: Annotated[User, Depends(get_current_user)]
):
    """(Protected) Endpoint to get a code review."""
    review_content = gemini_client.get_code_review(request.code, request.review_type)
    return CodeReviewResponse(
        review_type=request.review_type,
        review_content=review_content
    )

@app.post("/chat", response_model=ChatResponse)
async def chat_with_bot(
    request: ChatRequest,
    current_user: Annotated[User, Depends(get_current_user)]
):
    """(Protected) Endpoint for the chatbot."""
    reply = gemini_client.get_chat_response(request.message)
    return ChatResponse(reply=reply)

# --- Main entry point for uvicorn ---
if __name__ == "__main__":
    import uvicorn
    if not os.getenv("SECRET_KEY"):
        print("Warning: SECRET_KEY not set. Using a default insecure key.")
    if not os.getenv("GEMINI_API_KEY"):
        print("\n!!! WARNING: GEMINI_API_KEY environment variable is not set. !!!")
        print("The API will not work without it.\n")
        
    uvicorn.run(app, host="127.0.0.1", port=8000)