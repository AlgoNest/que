from flask import Flask, render_template, request
from scraper.extract_structure import extract_layout
from utils.prompt_builder import build_prompt
from ai.generate_code import generate_code

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form["url"]
        structure = extract_layout(url)
        prompt = build_prompt(structure)
        code = generate_code(prompt)

        return render_template(
            "preview.html",
            generated_html=code["html"]
        )

    return render_template("input.html")

if __name__ == "__main__":
    app.run(debug=True)

