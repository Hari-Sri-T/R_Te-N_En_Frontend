from flask import Flask, render_template, request
from gradio_client import Client

app = Flask(__name__)

# Initialize Gradio client for your Space
client = Client("HackHedron/Romanized-Telugu_to_Native-English_Translator")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/translate", methods=["GET","POST"])
def translate():
    user_input = request.form["text_input"]
    try:
        # Ensure input is passed as a list, not just a string
        result = client.predict(user_input = user_input, api_name="/predict")

        # Assuming Gradio returns a list with the following order:
        # 0 - original input
        # 1 - cleaned text
        # 2 - Telugu script
        # 3 - translated English text
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
