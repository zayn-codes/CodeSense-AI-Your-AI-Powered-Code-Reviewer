import streamlit as st
import requests
from streamlit_ace import st_ace
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Code Reviewer",
    page_icon="🤖",
    layout="wide"
)

# --- API Base URL ---
# Assumes the backend is running on the default port 8000
API_BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# --- CSS Loader ---
def load_css(file_name):
    """Loads a CSS file from the 'frontend' directory."""
    # Correct path assumes this script is in 'frontend/pages/'
    # Go up one level to 'frontend' and find 'style.css'
    try:
        css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), file_name)
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Could not find {file_name}. Make sure it's in the 'frontend' directory.")

load_css("style.css")

# --- Authentication Check ---
if "token" not in st.session_state:
    st.error("You must be logged in to access this page.")
    st.page_link("pages/2_Login.py", label="Go to Login", icon="🔑")
    st.stop()

# --- Page Title ---
st.title("🤖 AI Code Reviewer")
st.markdown("Paste your code below, select the review type, and let AI do the work.")

# --- UI Layout (2 Columns) ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Your Code")
    
    # Supported languages for syntax highlighting
    languages = [
        "python", "javascript", "java", "c_cpp", "csharp", "go", "ruby", "swift",
        "typescript", "php", "sql", "html", "css", "json", "yaml", "markdown"
    ]
    
    selected_language = st.selectbox("Language", options=languages, index=languages.index("python"))
    
    # Code Editor
    code = st_ace(
        language=selected_language,
        theme="tomorrow_night_blue",
        keybinding="vscode",
        font_size=14,
        height=400,
        show_gutter=True,
        show_print_margin=False,
        wrap=True,
        auto_update=True
    )

    review_type = st.selectbox(
        "Review Type",
        options=[
            ("General Purpose Review", "general"),
            ("Code Documentation Review", "documentation"),
            ("Competitive Programming (Time/Space)", "competitive")
        ],
        format_func=lambda x: x[0]  # Show the friendly name
    )
    
    submit_button = st.button("🚀 Get AI Review")

# --- API Call and Review Display ---
with col2:
    if submit_button:
        if not code:
            st.warning("Please paste some code to review.")
        else:
            with st.spinner("AI is analyzing your code... This may take a moment."):
                try:
                    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
                    payload = {
                        "code": code,
                        "review_type": review_type[1]  # Send the short name ("general", "docs", etc.)
                    }
                    
                    response = requests.post(
                        f"{API_BASE_URL}/review",
                        json=payload,
                        headers=headers
                    )
                    
                    if response.status_code == 200:
                        review_data = response.json()
                        # FIX 1: The backend model returns "review_content", not "review"
                        st.session_state.review_text = review_data.get("review_content")
                    elif response.status_code == 401:
                        st.error("Authentication failed. Your session may have expired.")
                        st.page_link("pages/2_Login.py", label="Go to Login", icon="🔑")
                    else:
                        st.error(f"An error occurred: {response.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the backend. Is it running?")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

    # --- **IMPROVED UI: Scrollable Review Box** ---
    if "review_text" in st.session_state:
        st.subheader("🤖 AI Review")
        # This creates a bordered container with a fixed height.
        # If content overflows, it becomes scrollable.
        with st.container(height=525, border=True):
            st.markdown(st.session_state.review_text)

# --- **IMPROVED UI: Stateful Chatbot Popover** ---
#st.popover("💬 Chat with AI", use_container_width=True)

with st.popover("💬 Chat with AI", use_container_width=True):
    # 1. Initialize chat history in session state
    if "popover_messages" not in st.session_state:
        st.session_state.popover_messages = [{"role": "assistant", "content": "How can I help you with your code?"}]

    # 2. Display all past messages
    # This container will hold the chat history
    with st.container(height=300):
        for msg in st.session_state.popover_messages:
            # Use custom CSS classes for styling
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user">
                    <div class="message-content">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant">
                    <div class="message-content">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)

    # 3. Handle new user input
    if prompt := st.chat_input("Ask a coding question..."):
        # Add user message to history
        st.session_state.popover_messages.append({"role": "user", "content": prompt})
        
        # Rerun to display the user's message immediately
        st.rerun()

    # 4. Generate AI response if the last message was from the user
    if st.session_state.popover_messages[-1]["role"] == "user":
        with st.spinner("AI is thinking..."):
            try:
                headers = {"Authorization": f"Bearer {st.session_state['token']}"}
                # FIX 2: The backend model expects "message", not "query"
                payload = {"message": st.session_state.popover_messages[-1]["content"]}
                
                response = requests.post(
                    f"{API_BASE_URL}/chat",
                    json=payload,
                    headers=headers
                )
                
                if response.status_code == 200:
                    # FIX 3: The backend model returns "reply", not "response"
                    chat_response = response.json().get("reply")
                    st.session_state.popover_messages.append({"role": "assistant", "content": chat_response})
                else:
                    st.session_state.popover_messages.append({"role": "assistant", "content": "Sorry, I had trouble connecting."})

            except Exception as e:
                st.session_state.popover_messages.append({"role": "assistant", "content": f"Error: {e}"})
        
        # Rerun to display the new assistant message
        st.rerun()