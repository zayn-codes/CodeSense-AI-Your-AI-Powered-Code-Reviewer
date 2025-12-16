import streamlit as st
import requests
from streamlit_ace import st_ace
import os
from pathlib import Path

# --- Handle Optional Dependency ---
try:
    from streamlit_diff_viewer import diff_viewer # type: ignore
    DIFF_VIEWER_AVAILABLE = True
except ImportError:
    DIFF_VIEWER_AVAILABLE = False

# --- Page Configuration ---
st.set_page_config(
    page_title="Code Reviewer",
    page_icon="🤖",
    layout="wide"
)

# --- API Base URL ---
API_BASE_URL = os.getenv("API_URL", "https://codesense-ai-your-ai-powered-code.onrender.com")

# --- CSS Loader ---
def load_css(file_name):
    try:
        css_path = Path(__file__).parent.parent / file_name
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css("style.css")

# --- Authentication Check ---
if "token" not in st.session_state:
    st.error("You must be logged in to access this page.")
    st.page_link("pages/2_Login.py", label="Go to Login", icon="🔑")
    st.stop()

# --- Initialize Editor State ---
if "editor_code" not in st.session_state:
    st.session_state.editor_code = ""

# --- Helper: Fetch Gist ---
def fetch_gist(gist_url):
    if "gist.github.com" not in gist_url:
        return None, "Invalid GitHub Gist URL."
    
    if "/raw" not in gist_url:
        raw_url = gist_url.rstrip("/") + "/raw"
    else:
        raw_url = gist_url
        
    try:
        response = requests.get(raw_url)
        if response.status_code == 200:
            return response.text, None
        else:
            return None, f"Failed to fetch. Status: {response.status_code}"
    except Exception as e:
        return None, f"Error: {e}"

# --- Page Title ---
st.title("🤖 AI Code Reviewer")
st.markdown("Paste your code, upload a file, or import from GitHub Gist.")

# --- UI Layout (2 Columns) ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input Code")

    with st.expander("📂 Import Code (File or Gist)", expanded=False):
        tab_file, tab_gist = st.tabs(["📄 Upload File", "🔗 GitHub Gist"])
        
        with tab_file:
            uploaded_file = st.file_uploader("Choose a code file", type=["py", "js", "java", "cpp", "c", "html", "css", "sql", "md", "txt"])
            if uploaded_file is not None:
                if st.button("Load File Content"):
                    try:
                        string_data = uploaded_file.getvalue().decode("utf-8")
                        st.session_state.editor_code = string_data
                        st.success("File loaded into editor!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error reading file: {e}")

        with tab_gist:
            gist_url = st.text_input("Paste GitHub Gist URL")
            if st.button("Fetch Gist"):
                if gist_url:
                    content, error = fetch_gist(gist_url)
                    if content:
                        st.session_state.editor_code = content
                        st.success("Gist loaded into editor!")
                        st.rerun()
                    else:
                        st.error(error)
                else:
                    st.warning("Please enter a URL.")

    languages = [
        "python", "javascript", "java", "c_cpp", "csharp", "go", "ruby", "swift",
        "typescript", "php", "sql", "html", "css", "json", "yaml", "markdown"
    ]
    
    selected_language = st.selectbox("Language", options=languages, index=languages.index("python"))
    
    code = st_ace(
        value=st.session_state.editor_code, 
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
    
    if code != st.session_state.editor_code:
        st.session_state.editor_code = code

    # MODIFICATION: Added "Explain This Code" to the list
    review_type = st.selectbox(
        "Review Type",
        options=[
            ("General Purpose Review", "general"),
            ("Code Documentation Review", "documentation"),
            ("Competitive Programming (Time/Space)", "competitive"),
            ("AI Code Refactor & Diff", "refactor"),
            ("Explain This Code", "explain")
        ],
        format_func=lambda x: x[0]
    )
    
    submit_button = st.button("🚀 Get AI Review")

# --- API Call and Review Display ---
with col2:
    if submit_button:
        if not code:
            st.warning("Please paste or import some code first.")
        else:
            with st.spinner("AI is analyzing your code..."):
                try:
                    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
                    selected_type_key = review_type[1]
                    
                    payload = {
                        "code": code,
                        "review_type": selected_type_key
                    }
                    
                    response = requests.post(
                        f"{API_BASE_URL}/review",
                        json=payload,
                        headers=headers
                    )
                    
                    if response.status_code == 200:
                        review_data = response.json()
                        st.session_state.review_result = review_data.get("review_content")
                        st.session_state.last_review_type = selected_type_key
                    elif response.status_code == 401:
                        st.error("Authentication failed.")
                        st.page_link("pages/2_Login.py", label="Go to Login", icon="🔑")
                    else:
                        st.error(f"An error occurred: {response.text}")
                        
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

    # --- Display Logic ---
    if "review_result" in st.session_state:
        st.subheader("🤖 AI Output")
        
        if st.session_state.get("last_review_type") == "refactor":
            st.markdown("#### Code Diff View")
            if DIFF_VIEWER_AVAILABLE:
                st.caption("Left: Original | Right: AI Refactored")
                diff_viewer(old_text=code, new_text=st.session_state.review_result, lang=selected_language)
            else:
                st.warning("`streamlit-diff-viewer` not found.")
                st.code(st.session_state.review_result, language=selected_language)
        else:
            with st.container(height=725, border=True):
                st.markdown(st.session_state.review_result)

# --- Chatbot Popover (Existing Code) ---

with st.popover("💬 Chat with AI", use_container_width=True):
    if "popover_messages" not in st.session_state:
        st.session_state.popover_messages = [{"role": "assistant", "content": "How can I help you with your code?"}]

    with st.container(height=300):
        for msg in st.session_state.popover_messages:
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

    if prompt := st.chat_input("Ask a coding question..."):
        st.session_state.popover_messages.append({"role": "user", "content": prompt})
        st.rerun()

    if st.session_state.popover_messages[-1]["role"] == "user":
        with st.spinner("AI is thinking..."):
            try:
                headers = {"Authorization": f"Bearer {st.session_state['token']}"}
                payload = {"message": st.session_state.popover_messages[-1]["content"]}
                
                response = requests.post(
                    f"{API_BASE_URL}/chat",
                    json=payload,
                    headers=headers
                )
                
                if response.status_code == 200:
                    chat_response = response.json().get("reply")
                    st.session_state.popover_messages.append({"role": "assistant", "content": chat_response})
                else:
                    st.session_state.popover_messages.append({"role": "assistant", "content": "Connection error."})

            except Exception as e:
                st.session_state.popover_messages.append({"role": "assistant", "content": f"Error: {e}"})
        

        st.rerun()
