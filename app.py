from flask import Flask, render_template, request
from gradio_client import Client

app = Flask(__name__)

# Initialize Gradio client for your Space
client = Client("HackHedron/Romanized-Telugu_to_Native-English_Translator")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    user_input = request.form["text_input"]
    try:
        result = client.predict(user_input, api_name="/predict")

        return render_template("translate.html", result={
            "original": result[0],
            "cleaned": result[1],
            "telugu": result[2],
            "translated": result[3]
        })
    except Exception as e:
        return render_template("translate.html", result={
            "translated": f"Error occurred: {str(e)}"
        })

if __name__ == "__main__":
    app.run(debug=True)

