import os
import json
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from openai import OpenAI

API_KEYS = [
    "8c485bc0789e4e998bc3ea2acf02b69c",
    "d7ad2c18bb7349b49644b89bc93713bd",
    "afa9af47c92b4f75a26643a5e26013dd",
    "a375c0a161094aff8708070cb95d3da3",
    "68ced62eac3c48eca9e451a63a45d2ac",
    "e58ed952cfac4686a297e94e1174c4e7"
]

BASE_URL = "https://api.aimlapi.com/v1"
MODEL_NAME = "google/gemma-3-12b-it"

MAX_INPUT_CHARS = 3000
AI_TIMEOUT = 8

def is_valid_url(url):
    try:
        u = urlparse(url)
        return u.scheme in ["http", "https"] and u.netloc
    except:
        return False


def build_prompt(content):
    return f"""
    You are a senior SaaS architect and production-grade full-stack engineer.

MODEL CONSTRAINTS (MANDATORY):
- Zero hallucination
- If uncertain → explicitly say "Not verified"
- Do NOT guess frameworks, APIs, or hosting behavior
- Prefer correctness over completeness

GOAL:
Generate a minimal, Apple-inspired (NOT copied) landing page and a Flask backend.
The output must be production-ready and compatible with Vercel serverless deployment.

DESIGN RULES:
- Static, calm, premium visual language
- No animations, no motion, no JS frameworks
- Large whitespace, centered layout
- Neutral colors (white, gray, black)
- System fonts only
- No icons unless requested
- No gradients or shadows

LANDING PAGE REQUIREMENTS:
- Clear value statement
- Clean HTML + Tailwind via CDN OR pure CSS
- No client-side JavaScript unless strictly necessary
- <<<{content}>>>


BACKEND REQUIREMENTS (FLASK):
- Python Flask only
- Stateless by default
- No background workers
- No paid services
- Must work as a Vercel serverless function

VERCEL COMPATIBILITY RULES:
- Use `app.py` entrypoint
- Flask app exposed as `app`
- No long-running processes
- No filesystem persistence (SQLite writes are not reliable)
- If storage is requested → warn clearly and suggest alternatives

PROJECT STRUCTURE (REQUIRED):
- app.py
- /templates/index.html
-/templates/preview.html
- 
- requirements.txt

CODE OUTPUT RULES:
- Output ONLY code blocks and minimal explanations
- Separate files clearly
- No markdown explanations inside code
- No emojis
- No filler text

INSPIRATION RULE:
- Layout may be inspired by Apple-style hierarchy and spacing
- Do NOT copy Apple wording, layout structure, or UI patterns directly
- Create original structure using similar design principles

FAILURE HANDLING:
- If a requirement conflicts with Vercel or Flask limitations → state the conflict explicitly
- Do NOT silently "make it work"

FINAL OUTPUT:
- Provide complete working example
- Ready to deploy without modification

{
        "frontend": "html, css, js if need",
        "backend": 'flask code',
}


"""

def get_client(api_key: str) -> OpenAI:
    """Initialize and return an OpenAI client with the given API key."""
    return OpenAI(base_url=BASE_URL, api_key=api_key)


def call_ai(prompt):
    for key in API_KEYS:
        try:
            client = get_client(key)
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                top_p=0.8,
                max_tokens=600,
                timeout=20,
            )

            content = response.choices[0].message.content.strip()

            try:
                clean_text = content.replace("```json", "").replace("```", "").strip()
                print(clean_text)
                return json.loads(clean_text)
            except json.JSONDecodeError:
                return {"error": "Invalid JSON format", "raw": content}

        except Exception as e:
            print(f"Error using key {key[:5]}...: {e}")
            continue  # Try next key

    return {"error": "All API calls failed or rate limited."}

def generate_code(prompt):
    # send prompt to AI model (OpenAI / local LLM)
    response = call_ai(prompt)

    return {
        "frontend": response["frontend"],
        "backend": response["backend"]
    }
