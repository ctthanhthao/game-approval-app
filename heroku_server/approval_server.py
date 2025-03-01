import os
import json
import requests
from flask import Flask, jsonify, request
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

app = Flask(__name__)

# Load game name and Slack channel from config.json
CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

config = load_config()
GAME_NAME = config.get("game_name", "Unknown Game")
SLACK_CHANNEL = config.get("slack_channel", "#general")

# Slack Bot Token
SLACK_TOKEN = os.getenv('SLACK_TOKEN')

if not SLACK_TOKEN:
    raise ValueError("SLACK_TOKEN environment variable is missing!")

slack_client = WebClient(token=SLACK_TOKEN)

APPROVAL_FILE = "approval_status.json"

@app.route('/')
def home():
    return "Game Approval App is running!", 200

def get_approval_status():
    """Reads the approval status from the file."""
    if os.path.exists(APPROVAL_FILE):
        with open(APPROVAL_FILE, "r") as f:
            data = json.load(f)
        return data.get("status", "pending")
    return "pending"

def set_approval_status(status):
    """Writes the approval status to the file."""
    with open(APPROVAL_FILE, "w") as f:
        json.dump({"status": status}, f)

@app.route('/game-started', methods=['POST'])
def game_started():
    """Sends a Slack message asking for game approval."""
    try:
        response = slack_client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text="🎮 Your son is trying to play a game. Approve?",
            attachments=[
                {
                    "text": "Approve or Deny?",
                    "fallback": "You can't choose an option",
                    "callback_id": "game_approval",
                    "color": "#3AA3E3",
                    "actions": [
                        {"name": "approve", "text": "✅ Allow", "type": "button", "value": "allow"},
                        {"name": "deny", "text": "⛔ Deny", "type": "button", "value": "deny"}
                    ]
                }
            ]
        )
        return jsonify({"message": "Approval request sent to Slack"}), 200
    except SlackApiError as e:
        return jsonify({"error": str(e.response['error'])}), 500

@app.route('/slack-interaction', methods=['POST'])
def slack_interaction():
    """Handles Slack button clicks (Approve/Deny)."""
    payload = request.form.get("payload")
    if not payload:
        return jsonify({"error": "No payload received"}), 400

    data = json.loads(payload)
    action_value = data["actions"][0]["value"]

    if action_value == "allow":
        set_approval_status("approved")
        message = "✅ Game Approved!"
    else:
        set_approval_status("denied")
        message = "⛔ Game Denied!"

    slack_client.chat_update(
        channel=data["channel"]["id"],
        ts=data["message_ts"],
        text=message,
        attachments=[]
    )
    
    return jsonify({"message": message}), 200

@app.route('/check-approval', methods=['GET'])
def check_approval():
    """Returns whether the game is approved or denied."""
    status = get_approval_status()
    return jsonify({"status": status}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
