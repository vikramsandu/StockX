"""
Given User Prompt, This agent extract the company name
and it's ticker symbol for further processing.
"""
import ast
import json
import subprocess


def parse_company_info(content: str):
    """
    Parses a response like: "Apple Inc., AAPL"
    into a tuple: ("Apple Inc.", "AAPL")
    """
    try:
        # Try parsing as Python literal first (e.g., tuple or dict string)
        parsed = ast.literal_eval(content)
        if isinstance(parsed, (list, tuple)) and len(parsed) == 2:
            return tuple(parsed)
        elif isinstance(parsed, dict) and 'name' in parsed and 'ticker' in parsed:
            return parsed['name'], parsed['ticker']
    except Exception:
        pass

    # If not a Python literal, parse manually
    parts = [p.strip() for p in content.split(",")]
    if len(parts) == 2:
        return parts[0], parts[1]

    return None  # fallback in case nothing worked


def extract_company_info(user_input: str,
                         prompt_system,  # Defines the system role
                         groq_key
                         ):
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": f"{prompt_system}"},
            {"role": "user", "content": f"{user_input}"}
        ]
    }

    response = subprocess.run(
        [
            "curl",
            "https://api.groq.com/openai/v1/chat/completions",
            "-H", f"Authorization: Bearer {groq_key}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(payload)
        ],
        capture_output=True,
        text=True
    )

    # Parse JSON output
    response_json = json.loads(response.stdout)
    content = response_json["choices"][0]["message"]["content"]
    content = parse_company_info(content)
    # print(content)
    if len(content) != 2:
        return None

    return content
