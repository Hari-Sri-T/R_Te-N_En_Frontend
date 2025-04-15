from flask import Flask, render_template, request
from gradio_client import Client

# Initialize Flask app
app = Flask(__name__)

# Initialize Gradio client
client = Client("http://127.0.0.1:7860/")  # This is your Gradio backend URL

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/translate", methods=["GET", "POST"])
def translate():
    result = {}
    if request.method == "POST":
        # Get user input from the form
        user_input = request.form["text_input"]
        print(f"Received input: {user_input}")
        
        try:
            # Send the input to the Gradio backend
            result = client.predict(
                user_input=user_input,   # The input to send
                api_name="/predict"      # API endpoint (default is "/predict")
            )
            print(f"Result from Gradio: {result}")
        except Exception as e:
            result = {"error": str(e)}
            print(f"Error occurred: {e}")
    
    # Render the result in the template
    return render_template("translate.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)