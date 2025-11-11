import streamlit as st
import os
from pathlib import Path  # Import Path

# --- Page Configuration ---
st.set_page_config(
    page_title="CodeSense-AI Home",
    page_icon="👋",
    layout="wide"
)

# --- CSS Loader (CORRECTED for this file) ---
def load_css(file_name):
    """Loads a CSS file from the 'frontend' directory."""
    try:
        # Get the directory of the current file (1_Home.py)
        # The CSS file is in the same directory.
        css_path = Path(__file__).parent / file_name
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Could not find {file_name} at {css_path}. Make sure it's in the 'frontend' directory.")

load_css("style.css")

# --- Page Content ---

st.title("Welcome to 🤖 CodeSense-AI")
st.subheader("Your AI-Powered Partner for Better Code")

st.markdown("""
CodeSense-AI is a full-stack application designed to help you write cleaner,
more efficient, and better-documented code.
""")

with st.container(border=True):
    st.header("✨ Features")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.subheader("General Review")
        st.markdown("Get a comprehensive review of your code for best practices, potential bugs, and logic improvements.")
        
    with c2:
        st.subheader("Documentation Analysis")
        st.markdown("Check your docstrings and comments for clarity, completeness, and adherence to standards.")
        
    with c3:
        st.subheader("Algorithm Analysis")
        st.markdown("Submit your competitive programming solutions to get Time and Space Complexity analysis (e.g., O(n log n)).")

st.markdown("""
### 🚀 Get Started

1.  **Register** a new account or **Login** if you're a returning user.
2.  Navigate to the **Code Reviewer** page.
3.  Paste your code, select your review type, and get instant AI feedback!
""")

st.page_link("pages/2_Login.py", label="Login or Register", icon="🔑")

# --- Footer ---
st.markdown("---")
st.markdown("Built with `FastAPI`, `Streamlit`, and the `Google Gemini API`.")
