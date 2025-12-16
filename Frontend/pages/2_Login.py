import streamlit as st
import requests
import os
from pathlib import Path

# --- Page Configuration ---
st.set_page_config(
    page_title="Login - CodeSense-AI",
    page_icon="🔐",
    layout="centered"
)

# --- API Base URL ---
API_BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# --- CSS Loader ---
def load_css(file_name):
    try:
        css_path = Path(__file__).parent.parent / file_name
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css("style.css")

# --- Page Title ---
st.title("🔐 Login")
st.markdown("Welcome back to **CodeSense-AI**.")

# --- Helper Functions ---

def handle_login(username, password):
    """Attempts to log in via the API and redirects on success."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/token",
            data={"username": username, "password": password}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            # Set Session State
            st.session_state.token = token_data["access_token"]
            st.session_state.username = username
            
            # Success Message
            st.success("Login successful!")
            
            # --- MODIFICATION: Instant Redirect ---
            st.switch_page("pages/3_Code_Reviewer.py")
            
        elif response.status_code == 401:
            st.error("Incorrect username or password.")
        else:
            st.error(f"Login failed. Server returned: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        st.error("Failed to connect to the backend. Is it running?")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def handle_register(username, password, confirm_password):
    """Attempts to register a new user."""
    if not username or not password:
        st.warning("Please enter both username and password.")
        return
    if password != confirm_password:
        st.error("Passwords do not match.")
        return
        
    try:
        response = requests.post(
            f"{API_BASE_URL}/register",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            st.success("Registration successful! Please go to the Login tab.")
            st.balloons()
        elif response.status_code == 400:
            st.error("Username already taken.")
        else:
            st.error(f"Registration failed: {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("Failed to connect to the backend.")
    except Exception as e:
        st.error(f"An error occurred: {e}")


# --- UI Tabs ---
tab1, tab2 = st.tabs(["➡️ Login", "🆕 Register"])

# --- Login Tab ---
with tab1:
    with st.form("login_form"):
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        login_btn = st.form_submit_button("Login", type="secondary")

        if login_btn:
            handle_login(login_user, login_pass)

# --- Register Tab ---
with tab2:
    with st.form("register_form"):
        reg_user = st.text_input("Choose Username", key="reg_user")
        reg_pass = st.text_input("Choose Password", type="password", key="reg_pass")
        reg_conf = st.text_input("Confirm Password", type="password", key="reg_conf")
        reg_btn = st.form_submit_button("Create Account")

        if reg_btn:
            handle_register(reg_user, reg_pass, reg_conf)

# --- Footer Link ---
st.markdown("---")
st.page_link("1_Home.py", label="Back to Home", icon="🏠")