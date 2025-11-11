import streamlit as st
import requests
import json

# --- Config ---
st.set_page_config(
    page_title="Login - AI Code Reviewer",
    page_icon="🔐",
    layout="centered"
)

# --- API URL ---
BACKEND_URL = "http://127.0.0.1:8000"

# --- Load CSS ---
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass # Silently fail if CSS not found on subpages, as 1_Home.py loads it.

load_css("style.css") # Load CSS for consistent styling

# --- Initialize Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "token" not in st.session_state:
    st.session_state.token = ""

# --- Main Logic ---

if st.session_state.logged_in:
    st.title(f"Logged in as {st.session_state.username}")
    st.success("You are already logged in.")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.token = ""
        st.rerun() # Rerun the page to show the login form
        
    st.page_link("pages/3_Code_Reviewer.py", label="Go to App")

else:
    st.title("Login or Register")
    
    login_tab, register_tab = st.tabs(["🔐 Login", "📝 Register"])

    # --- Login Tab ---
    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            login_button = st.form_submit_button("Login")

            if login_button:
                if not username or not password:
                    st.error("Please enter both username and password.")
                else:
                    try:
                        # FastAPI's OAuth2PasswordRequestForm expects form data
                        login_data = {
                            "username": username,
                            "password": password
                        }
                        response = requests.post(f"{BACKEND_URL}/token", data=login_data)

                        if response.status_code == 200:
                            token_data = response.json()
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.session_state.token = token_data["access_token"]
                            st.success("Login Successful!")
                            st.rerun() # Rerun to show logged-in state
                        elif response.status_code == 401:
                            st.error("Incorrect username or password.")
                        else:
                            st.error(f"An error occurred: {response.text}")
                    except requests.ConnectionError:
                        st.error("Could not connect to the backend API. Is it running?")
                    except Exception as e:
                        st.error(f"An unknown error occurred: {e}")

    # --- Register Tab ---
    with register_tab:
        with st.form("register_form"):
            reg_username = st.text_input("Choose a Username", key="reg_username")
            reg_password = st.text_input("Choose a Password", type="password", key="reg_password")
            register_button = st.form_submit_button("Register")

            if register_button:
                if not reg_username or not reg_password:
                    st.error("Please enter both username and password.")
                else:
                    try:
                        # The /register endpoint expects JSON
                        register_data = {
                            "username": reg_username,
                            "password": reg_password
                        }
                        response = requests.post(f"{BACKEND_URL}/register", json=register_data)

                        if response.status_code == 200:
                            st.success("Registration successful! Please go to the Login tab.")
                        elif response.status_code == 400:
                            st.error("Username already registered.")
                        else:
                            st.error(f"An error occurred: {response.text}")
                    except requests.ConnectionError:
                        st.error("Could not connect to the backend API. Is it running?")
                    except Exception as e:
                        st.error(f"An unknown error occurred: {e}")