import os
import google.generativeai as genai
from models import ReviewType
import re

# --- Prompts ---

CP_REVIEW_PROMPT = """
You are an expert competitive programming (CP) analyst and coach.
Analyze the following code written for a competitive programming problem.
Please provide your analysis in the following structured format:

1.  **Algorithm:** A brief, 1-2 sentence explanation of the algorithm being used.
2.  **Time Complexity:** The time complexity (Big O). Briefly explain why.
3.  **Space Complexity:** The space complexity (Big O). Briefly explain why.
4.  **Explanation:** A step-by-step explanation of the logic.
5.  **Optimization:** If applicable, how to optimize it.

Code:
```
{code}
```
"""

DOC_REVIEW_PROMPT = """
You are a senior software developer acting as a code reviewer.
Review the following code for its documentation quality.

1.  **Overall Quality:** Brief assessment.
2.  **Missing Documentation:** List missing comments/docstrings.
3.  **Clarity:** Are existing docs clear?
4.  **Example:** Write an example of a good docstring for this code.

Code:
```
{code}
```
"""

GENERAL_REVIEW_PROMPT = """
You are a helpful AI code reviewer. Provide a general review.

1.  **Bugs or Errors:** Identify potential bugs.
2.  **Readability:** Improvements for variable names/structure.
3.  **Best Practices:** Does it follow standards (e.g., PEP 8)?
4.  **Suggestions:** Concrete suggestions for improvement.

Code:
```
{code}
```
"""

REFACTOR_REVIEW_PROMPT = """
You are an expert software engineer.
Refactor the following code to fix any bugs, improve readability, and apply best practices.
Respond ONLY with the complete, refactored code.
Do not include any explanations.
Do not include markdown code block markers (like ```python or ```).
Just return the raw code text.

Code:
{code}
"""

# MODIFICATION: New Prompt for Explanation
EXPLAIN_REVIEW_PROMPT = """
You are a helpful programming tutor. 
Explain the following code step-by-step in plain English. 
Focus on the logic, the flow, and what each major part is trying to achieve. 
Use markdown and bullet points for clarity. 
Do not just rewrite the code; explain *why* it works.

Code: 
{code}
"""

CHAT_PROMPT = """
You are a helpful AI assistant specializing in programming.
Answer the user's question clearly.
User's question: {message}
"""


# --- Gemini Client ---

def configure_gemini():
    """Configures the Gemini API."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

def get_gemini_model():
    """Initializes and returns the Gemini model."""
    return genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')

def clean_refactored_code(text: str) -> str:
    """Helper to strip markdown code blocks."""
    pattern = r"^```[a-zA-Z]*\n"
    text = re.sub(pattern, "", text)
    text = text.replace("```", "")
    return text.strip()

def get_code_review(code: str, review_type: ReviewType) -> str:
    """Gets a code review from the Gemini API."""
    model = get_gemini_model()
    
    prompt = ""
    if review_type == "general":
        prompt = GENERAL_REVIEW_PROMPT.format(code=code)
    elif review_type == "documentation":
        prompt = DOC_REVIEW_PROMPT.format(code=code)
    elif review_type == "competitive":
        prompt = CP_REVIEW_PROMPT.format(code=code)
    elif review_type == "refactor":
        prompt = REFACTOR_REVIEW_PROMPT.format(code=code)
    elif review_type == "explain":  # MODIFICATION: Handle new type
        prompt = EXPLAIN_REVIEW_PROMPT.format(code=code)
    else:
        raise ValueError("Invalid review type")

    try:
        response = model.generate_content(prompt)
        content = response.text
        
        if review_type == "refactor":
            content = clean_refactored_code(content)
            
        return content
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "An error occurred while generating the review. Please try again."

def get_chat_response(message: str) -> str:
    """Gets a chat response from the Gemini API."""
    model = get_gemini_model()
    prompt = CHAT_PROMPT.format(message=message)
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "An error occurred while generating the response. Please try again."