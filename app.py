from flask import Flask, render_template, request
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API key securely
api_key = os.getenv("GROQ_API_KEY")

print("Loaded API Key successfuly")

if not api_key:
    raise ValueError("No GROQ_API_KEY found in environment variables")

client = Groq(api_key=api_key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/try")
def try_page():
    return render_template("try.html")


@app.route("/generate", methods=["POST"])
def generate():
    try:
        user_text = request.form["user_input"]

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": user_text}
            ]
        )

        output = response.choices[0].message.content

        return render_template("result.html", result=output)

    except Exception as e:
        return render_template("error.html", error=str(e))


if __name__ == "__main__":
    app.run(debug=True)
