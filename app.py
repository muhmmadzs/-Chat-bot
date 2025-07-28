"""
Flask application for a GPT‑based chatbot.

This server exposes two routes:

* `GET /` – Render the chat interface.
* `POST /chat` – Accept a JSON payload containing past conversation messages
  and return a new assistant reply generated using OpenAI’s ChatCompletion API.

Messages are expected to be dictionaries with a `role` ("user" or "assistant")
and a `content` string.  The server prepends a configurable system prompt
before forwarding the conversation to the API.  Only the most recent
`history_length` messages are retained to limit token usage.

Before running this application you must set the `OPENAI_API_KEY`
environment variable.  You can optionally set `MODEL_NAME` and adjust the
system prompt in this file.
"""

import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

try:
    import openai
except ImportError:
    raise ImportError(
        "The `openai` library is required. Please install it with `pip install openai`."
    )


# Load environment variables from a .env file if present
load_dotenv()

# Create the Flask app
app = Flask(__name__)

# Read the API key from the environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print(
        "Warning: OPENAI_API_KEY is not set. The application will not be able to communicate with the OpenAI API."
    )
openai.api_key = OPENAI_API_KEY

# Select the model. Use environment variable if provided, default to gpt-3.5-turbo
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

# Configure the system prompt. Adjust these lines to customise the assistant’s behaviour.
system_prompt = (
    "You are a helpful assistant for ExampleCorp.\n"
    "You follow company policies, answer accurately, and maintain a polite, professional tone.\n"
    "If you don't know an answer, say you are unsure rather than guessing."
)

# Limit how many past messages are sent to the model.  Keeping this small
# reduces token usage while retaining conversation context.
history_length = 10


@app.route("/")
def index() -> str:
    """Render the chat interface."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat() -> tuple:
    """Handle chat requests from the frontend.

    Expects a JSON payload with a `messages` field: a list of dicts with keys
    `role` and `content`.  Returns a JSON response containing the assistant’s
    reply or an error message.
    """
    if not OPENAI_API_KEY:
        return (
            jsonify(
                {
                    "error": "API key not configured. Please set OPENAI_API_KEY on the server.",
                    "response": None,
                }
            ),
            500,
        )

    data = request.get_json(silent=True)
    if not data or "messages" not in data:
        return (
            jsonify(
                {
                    "error": "Invalid payload. Please send a JSON object with a 'messages' field.",
                    "response": None,
                }
            ),
            400,
        )

    user_messages = data["messages"]
    # Validate message format
    if not isinstance(user_messages, list) or any(
        not isinstance(m, dict) or "role" not in m or "content" not in m
        for m in user_messages
    ):
        return (
            jsonify(
                {
                    "error": "Each message must be a dict with 'role' and 'content'.",
                    "response": None,
                }
            ),
            400,
        )

    # Build conversation with system prompt and recent history
    conversation = [
        {"role": "system", "content": system_prompt},
    ]
    # Only include the last `history_length` messages
    conversation.extend(user_messages[-history_length:])

    # Call the OpenAI ChatCompletion API
    try:
        completion = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=conversation,
        )
        reply_content = completion.choices[0].message["content"]
        return jsonify({"response": reply_content, "error": None})
    except Exception as e:
        # Handle API errors gracefully
        return (
            jsonify(
                {
                    "error": f"There was an error communicating with the language model: {e}",
                    "response": None,
                }
            ),
            500,
        )


if __name__ == "__main__":
    # Run the app. In production you might use a WSGI server instead.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)