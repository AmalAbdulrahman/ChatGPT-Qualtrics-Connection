from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
import time

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = Flask(__name__)


@app.route("/")
def index():
    participant_id = request.args.get("participant_id", "unknown")
    return render_template("chat.html", participant_id=participant_id)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")
    participant_id = data.get("participant_id", "unknown")

    response = client.chat.completions.create(model="gpt-4",
                                              messages=[{
                                                  "role": "user",
                                                  "content": user_message
                                              }])

    bot_response = response.choices[0].message.content

    # Log the interaction
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("chat_logs.txt", "a") as log_file:
        log_file.write(f"[{timestamp}] ID: {participant_id}\n")
        log_file.write(f"User: {user_message}\n")
        log_file.write(f"Bot: {bot_response}\n\n")

    return jsonify({"response": bot_response})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
