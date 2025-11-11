import os
import google.generativeai as genai
from models import ReviewType

# --- Prompts ---

# This prompt is key for the Competitive Programming feature
CP_REVIEW_PROMPT = """
You are an expert competitive programming (CP) analyst and coach.
Analyze the following code written for a competitive programming problem.
Please provide your analysis in the following structured format:

1.  **Algorithm:** A brief, 1-2 sentence explanation of the algorithm being used (e.g., "This is a dynamic programming solution for the knapsack problem," "This uses a breadth-first search to find the shortest path," etc.).

2.  **Time Complexity:** The time complexity of the algorithm, in Big O notation (e.g., O(n log n)). Briefly explain why.

3.  **Space Complexity:** The space complexity of the algorithm, in Big O notation (e.g., O(n)). Briefly explain why.

4.  **Explanation:** A more detailed, step-by-step explanation of the code's logic. How does it work?

5.  **Optimization (Optional):** If you see a clear way to optimize the code, mention it.

Here is the code:
```
{code}
```
"""

# This prompt is for the Documentation review
DOC_REVIEW_PROMPT = """
You are a senior software developer acting as a code reviewer.
Your *only* task is to review the following code for its documentation quality.
Do not comment on the logic, style, or performance unless it's directly related to the documentation.

Please provide your review in the following structured format:

1.  **Overall Documentation Quality:** A brief assessment (e.g., Excellent, Good, Needs Improvement, Poor).
2.  **Missing Documentation:** List any functions, classes, or complex logic blocks that are missing comments or docstrings.
3.  **Clarity of Existing Docs:** Are the existing comments clear, concise, and accurate?
4.  **Example of Good Docstring:** Write one example of a high-quality docstring for one of the functions in this code, showing how it *should* be done.

Here is the code:
```
{code}
```
"""

# This prompt is for the General review
GENERAL_REVIEW_PROMPT = """
You are a helpful AI code reviewer.
Provide a general review of the following code.
Look for the following:

1.  **Bugs or Errors:** Identify any potential bugs, logic errors, or edge cases that might not be handled.
2.  **Readability:** How easy is the code to read and understand? Suggest improvements for variable names, function names, and code structure.
3.  **Best Practices:** Does the code follow common best practices for the language? (e.g., Python PEP 8).
4.  **Suggestions for Improvement:** Offer concrete suggestions to make the code more efficient, more robust, or cleaner.

Please provide your review in a clear, constructive, and easy-to-understand format.

Here is the code:
```
{code}
```
"""

CHAT_PROMPT = """
You are a helpful AI assistant specializing in programming and computer science.
Answer the user's question clearly and concisely.
If the user asks for code, provide it in a code block.

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

def get_code_review(code: str, review_type: ReviewType) -> str:
    """Gets a code review from the Gemini API based on the review type."""
    model = get_gemini_model()
    
    prompt = ""
    if review_type == "general":
        prompt = GENERAL_REVIEW_PROMPT.format(code=code)
    elif review_type == "documentation":
        prompt = DOC_REVIEW_PROMPT.format(code=code)
    elif review_type == "competitive":
        prompt = CP_REVIEW_PROMPT.format(code=code)
    else:
        raise ValueError("Invalid review type")

    try:
        response = model.generate_content(prompt)
        return response.text
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