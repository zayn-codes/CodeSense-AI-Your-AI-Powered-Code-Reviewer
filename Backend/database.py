import sqlite3
import os
from passlib.context import CryptContext

# Configuration
DATABASE_URL = "code_reviewer.db"

# --- Password Hashing Setup ---
#
#  We are now ONLY using "argon2".
#  We have completely removed "bcrypt" from the schemes list
#  to match our clean environment.
#
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# --- Hashing Utility ---

def verify_password(plain_password: str, hashed_password: str):
    """
    Checks if a plain password matches a hashed one.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    """
    Hashes a password for storage.
    """
    return pwd_context.hash(password)

# --- Database Initialization ---

def init_db():
    """Initializes the database and creates the user table if it doesn't exist."""
    if os.path.exists(DATABASE_URL):
        # print("Database already exists.")
        pass
    else:
        print("Creating new database...")
        conn = None
        try:
            conn = sqlite3.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            # Create user table
            cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL
            );
            """)
            print("User table created successfully.")
            
            conn.commit()
            
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
        finally:
            if conn:
                conn.close()

# --- User Management Functions ---

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def get_user(username: str):
    """Fetches a user by username from the database."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user:
            return dict(user)
        return None
    except sqlite3.Error as e:
        print(f"Database error in get_user: {e}")
        return None
    finally:
        if conn:
            conn.close()

def create_user(username: str, password: str):
    """Creates a new user in the database."""
    conn = None
    try:
        hashed_password = get_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, hashed_password) VALUES (?, ?)",
            (username, hashed_password)
        )
        conn.commit()
        return get_user(username)
        
    except sqlite3.IntegrityError:
        # This catches the 'UNIQUE NOT NULL' constraint violation
        return "Username already exists"
    except sqlite3.Error as e:
        print(f"Database error in create_user: {e}")
        return None
    finally:
        if conn:
            conn.close()