def generate_code(prompt):
    # send prompt to AI model (OpenAI / local LLM)
    response = ai_client(prompt)

    return {
        "html": response["html"],
        "css": response.get("css", ""),
        "js": response.get("js", "")
    }
