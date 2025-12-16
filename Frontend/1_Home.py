import streamlit as st
import os
from pathlib import Path

# --- Page Configuration ---
st.set_page_config(
    page_title="CodeSense-AI",
    page_icon="⚡",
    layout="wide"
)

# --- CSS Loader ---
def load_css(file_name):
    try:
        css_path = Path(__file__).parent / file_name
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css("style.css")

# --- Hero Section ---
st.title("⚡ CodeSense-AI")
st.subheader("The Ultimate AI Companion for Developers")

st.markdown("""
Elevate your coding workflow with **CodeSense-AI**. 
Whether you need to debug a script, optimize an algorithm, or refactor legacy code, 
our Gemini-powered engine provides instant, professional-grade feedback.
""")

# --- Main Action Button ---
# If logged in, show "Go to App". If not, show "Get Started"
if "token" in st.session_state:
    if st.button("🚀 Go to Code Reviewer", type="secondary"):
        st.switch_page("pages/3_Code_Reviewer.py")
else:
    if st.button("✨ Get Started (Login / Register)", type="secondary"):
        st.switch_page("pages/2_Login.py")

st.markdown("---")

# --- Features Grid ---
st.markdown("### 🛠️ Powerful Features")

# CSS for the grid layout is handled in style.css, but we use columns here for structure
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("#### 🐛 Bug Hunter")
        st.caption("General Review")
        st.write("Detect bugs, logic errors, and security vulnerabilities before they hit production.")

    with st.container(border=True):
        st.markdown("#### 🔄 AI Refactor")
        st.caption("Diff View")
        st.write("Let AI rewrite your code for you. View changes side-by-side with a professional diff viewer.")

with col2:
    with st.container(border=True):
        st.markdown("#### 📝 Doc Generator")
        st.caption("Documentation")
        st.write("Automatically generate clear, concise docstrings and comments for your functions and classes.")

    with st.container(border=True):
        st.markdown("#### 🧠 Code Tutor")
        st.caption("Explain This Code")
        st.write("Confused by a complex block? Get a step-by-step plain English explanation of the logic.")

with col3:
    with st.container(border=True):
        st.markdown("#### ⚡ Algo Optimizer")
        st.caption("Competitive Programming")
        st.write("Analyze Time & Space Complexity (Big O) and get suggestions to optimize performance.")

    with st.container(border=True):
        st.markdown("#### 📂 Easy Import")
        st.caption("File & Gist Support")
        st.write("Upload local files (`.py`, `.js`, etc.) or import directly from GitHub Gists.")

st.markdown("---")
st.markdown("##### 🔒 Secure & Private")
st.caption("Your data is safe. We use industry-standard Argon2 hashing and JWT authentication.")