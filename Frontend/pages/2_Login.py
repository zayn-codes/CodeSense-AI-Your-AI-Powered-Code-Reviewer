import streamlit as st
import requests
import os
from pathlib import Path  # Import Path

# --- Page Configuration ---
st.set_page_config(
    page_title="Login - CodeSense-AI",
    page_icon="🔑",
    layout="centered"
)

# --- API Base URL ---
API_BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# --- CSS Loader (CORRECTED for this file) ---
def load_css(file_name):
    """Loads a CSS file from the 'frontend' directory."""
    try:
        # Get the directory of the current file (e.g., .../frontend/pages)
        # Go up one level to the 'frontend' directory
        css_path = Path(__file__).parent.parent / file_name
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Could not find {file_name} at {css_path}. Make sure it's in the 'frontend' directory.")

load_css("style.css")

# --- Page Title ---
st.title("Welcome to 🤖 CodeSense-AI")
st.subheader("Login or Register to Continue")

# --- UI Tabs ---
tab1, tab2 = st.tabs(["Login", "Register"])

# --- Login Tab ---
with tab1:
    with st.form("login_form"):
        st.markdown("#### Existing User Login")
        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")
        login_button = st.form_submit_button("Login")

        if login_button:
            if not login_username or not login_password:
                st.warning("Please enter both username and password.")
            else:
                try:
                    # FastAPI's token endpoint expects form data
                    response = requests.post(
                        f"{API_BASE_URL}/token",
                        data={"username": login_username, "password": login_password}
                    )
                    
                    if response.status_code == 200:
                        token_data = response.json()
                        st.session_state.token = token_data["access_token"]
                        st.session_state.username = login_username
                        st.success("Login successful! Redirecting to the app...")
                        st.page_link("pages/3_Code_Reviewer.py", label="Go to Code Reviewer", icon="🚀")
                        # st.switch_page("pages/3_Code_Reviewer.py") # Use if available
                    elif response.status_code == 401:
                        st.error("Incorrect username or password.")
                    else:
                        st.error(f"An error occurred: {response.text}")
                
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the backend. Is it running?")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

# --- Registration Tab ---
with tab2:
    with st.form("register_form"):
        st.markdown("#### New User Registration")
        reg_username = st.text_input("Choose a Username", key="reg_user")
        reg_password = st.text_input("Choose a Password", type="password", key="reg_pass")
        reg_password_confirm = st.text_input("Confirm Password", type="password", key="reg_pass_confirm")
        register_button = st.form_submit_button("Register")

        if register_button:
            if not reg_username or not reg_password or not reg_password_confirm:
                st.warning("Please fill out all fields.")
            elif reg_password != reg_password_confirm:
                st.error("Passwords do not match.")
            else:
                try:
                    payload = {"username": reg_username, "password": reg_password}
                    response = requests.post(
                        f"{API_BASE_URL}/register",
                        json=payload
                    )
                    
                    if response.status_code == 200:
                        st.success("Registration successful! Please log in.")
                    elif response.status_code == 400:
                        st.error("Username already registered. Please choose another.")
                    else:
                        st.error(f"An error occurred: {response.text}")

                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the backend. Is it running?")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
