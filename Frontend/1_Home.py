import streamlit as st
import os

# --- Page Config ---
st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load CSS ---
def load_css(file_name):
    """Loads a CSS file from the /frontend directory."""
    # We are in the frontend/ directory, but script runs from root
    # So we need to be careful with paths.
    # Let's assume the script is run from the `frontend` directory.
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Could not find {file_name}. Make sure it's in the frontend/ directory.")

load_css("style.css")

# --- Initialize Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "token" not in st.session_state:
    st.session_state.token = ""

# --- Sidebar ---
st.sidebar.title("Navigation")

if st.session_state.logged_in:
    st.sidebar.write(f"Logged in as: **{st.session_state.username}**")
    st.sidebar.page_link("pages/3_Code_Reviewer.py", label="Code Reviewer")
    st.sidebar.page_link("pages/2_Login.py", label="Logout")
else:
    st.sidebar.page_link("pages/2_Login.py", label="Login / Register")


# --- Main Page Content ---

st.title("Welcome to the AI Code Reviewer 🤖")
st.subheader("Your intelligent partner for cleaner, faster, and smarter code.")

st.markdown("""
This tool, powered by Google's Gemini API, helps you write better code by providing
detailed reviews, documentation analysis, and competitive programming insights.
""")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True, height=250):
        st.markdown("### 🚀 General Review")
        st.write("Get a comprehensive review of your code for bugs, readability, and best practices.")

with col2:
    with st.container(border=True, height=250):
        st.markdown("### 📚 Doc Review")
        st.write("Analyze the quality and completeness of your code's documentation.")

with col3:
    with st.container(border=True, height=250):
        st.markdown("### 🏆 CP Analysis")
        st.write("Understand the time/space complexity and algorithm of your competitive programming solutions.")


st.markdown("---")
if st.session_state.logged_in:
    st.success("You are logged in.")
    st.page_link("pages/3_Code_Reviewer.py", label="Go to the Code Reviewer", icon="➡️")
else:
    st.info("Please **Login** or **Register** to get started.")
    st.page_link("pages/2_Login.py", label="Login / Register", icon="➡️")