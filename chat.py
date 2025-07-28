from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("MIMO_OPENAI_API_KEY")
MIMO_URL = "https://ai.mimo.org/v1/openai/message"
HEADERS = {"api-key": API_KEY}

thread_id = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    global thread_id
    data = request.get_json()
    message = data.get("message")

    body = {"message": message}
    if thread_id:
        body["threadId"] = thread_id

    try:
        response = requests.post(MIMO_URL, headers=HEADERS, json=body)
        json_data = response.json()
        thread_id = json_data.get("threadId")
        return jsonify({"response": json_data.get("response")})
    except Exception as e:
        return jsonify({"response": f"❌ Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
