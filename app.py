from flask import Flask, render_template, request
import requests

# Initialize Flask app
app = Flask(__name__)

# Your Gradio backend URL (no trailing slash)
GRADIO_BACKEND_URL = "https://9718-2402-e280-3e0b-7b4-44f6-515d-168d-37b5.ngrok-free.app"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/translate", methods=["GET", "POST"])
def translate():
    result = {}
    if request.method == "POST":
        user_input = request.form["text_input"]
        print(f"Received input: {user_input}")
        
        try:
            # Send POST request to Gradio backend
            response = requests.post(
                f"{GRADIO_BACKEND_URL}/run/predict",
                headers={"Content-Type": "application/json"},
                json={"data": [user_input]}
            )

            if response.status_code == 200:
                result_data = response.json()["data"]
                result["original"] = result_data[0]
                result["cleaned"] = result_data[1]
                result["telugu"] = result_data[2]
                result["translated"] = result_data[3]
                print("Gradio Response:", result)
            else:
                result["translated"] = f"Error: Status {response.status_code}"
        except Exception as e:
            result["translated"] = f"Error occurred: {e}"
            print("Exception:", e)

    return render_template("translate.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
