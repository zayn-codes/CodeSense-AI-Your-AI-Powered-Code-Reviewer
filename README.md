🤖 CodeSense-AI: Your AI-Powered Code Reviewer

CodeSense-AI is a full-stack web application that leverages the Google Gemini API to provide intelligent, on-demand code reviews. Built with a modern FastAPI backend and an interactive Streamlit frontend, this tool helps developers improve code quality, document standards, and analyze algorithm complexity.

✨ Features

Secure User Authentication: JWT-based login and registration system.

Persistent User Data: User profiles are securely stored in a database.

Multi-Type Code Analysis:

General Review: Checks for best practices, potential bugs, and logic improvements.

Documentation Review: Analyzes docstrings and comments for clarity and completeness.

Competitive Programming: Provides Time and Space Complexity analysis (e.g., O(n log n)) and explains the user's algorithm.

Interactive AI Chatbot: A popover chat assistant for any coding-related questions.

Modern UI: A clean, responsive interface built with Streamlit, including an ACE code editor with syntax highlighting.

Scalable Backend: A robust API built with FastAPI, ready to handle concurrent requests.

🚀 Tech Stack

Frontend: Streamlit

Backend: FastAPI

AI Model: Google Gemini

Database: SQLite

Authentication: JWT (python-jose)

Password Hashing: Argon2 (passlib)

Deployment: Render

📁 File Structure

ai-code-reviewer-app/
│
├── backend/
│   ├── .env.example        # Environment variable template
│   ├── code_reviewer.db    # Local SQLite database
│   ├── database.py         # DB logic, user management, hashing
│   ├── gemini_client.py    # All Gemini API logic and prompts
│   ├── main.py             # FastAPI application
│   ├── models.py           # Pydantic models for API
│   └── requirements.txt    # Backend Python packages
│
└── frontend/
    ├── pages/
    │   ├── 2_Login.py      # Login & Register page
    │   └── 3_Code_Reviewer.py # Main app page
    │
    ├── 1_Home.py           # Streamlit landing page
    ├── requirements.txt    # Frontend Python packages
    └── style.css           # Custom CSS for styling


⚙️ Local Setup

Prerequisites

Python 3.10+

A Google Gemini API Key.

A separate terminal for the backend and frontend.

1. Backend Setup

Navigate to the backend folder:

cd backend


Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # (or .\venv\Scripts\activate on Windows)


Install dependencies:

pip install -r requirements.txt


Set up environment variables:

Copy .env.example to a new file named .env.

Edit .env and add your GEMINI_API_KEY.

Generate a SECRET_KEY using:

python -c "import secrets; print(secrets.token_hex(32))"


Paste the generated key into your .env file.

Run the backend server:

uvicorn main:app --reload


The API will be running at http://127.0.0.1:8000.

2. Frontend Setup

Open a new terminal and navigate to the frontend folder:

cd frontend


Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # (or .\venv\Scripts\activate on Windows)


Install dependencies:

pip install -r requirements.txt


Run the frontend app:

streamlit run 1_Home.py


The app will open in your browser at http://localhost:8501.

☁️ Deployment

This application is configured for deployment on Render as two separate "Web Services" using a monorepo structure.

Backend Service:

Root Directory: backend

Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT

A Persistent Disk is required to store the SQLite database.

Env Vars: GEMINI_API_KEY, SECRET_KEY, DB_DIR (e.g., /var/data).

Frontend Service:

Root Directory: frontend

Start Command: streamlit run 1_Home.py --server.port $PORT --server.address 0.0.0.0

Env Vars: API_URL (set to the URL of the deployed backend service).

License

This project is licensed under the MIT License.
