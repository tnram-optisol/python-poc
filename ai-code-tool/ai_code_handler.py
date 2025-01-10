import openai
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
# Load OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_project_code(project,frontend, backend, database):
    """Generates project code based on the user's requirements using ChatGPT models."""
    prompt = f"""
    Create a {project} with the following:
    - Frontend: {frontend}
    - Backend: {backend}
    - Database: {database}

    Organize the project into files and folders, and return code snippets 
    for each file in a JSON-like structure, e.g.:
    {{
        "frontend/index.js": "code for index.js",
        "backend/app.py": "code for app.py",
        "backend/models.py": "code for models.py"
    }}
    """

    print(prompt)

    # Use the chat/completions endpoint with `gpt-3.5-turbo` or `gpt-4`
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Switch to "gpt-4" if needed
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates project code."},
            {"role": "user", "content": prompt}
        ],
        temperature=1
    )

    # Extract the AI's reply
    ai_reply = response["choices"][0]["message"]["content"].strip()

    try:
        return eval(ai_reply)  # Convert JSON-like string to Python dict
    except Exception as e:
        raise ValueError(f"Failed to parse AI response: {str(e)}")
