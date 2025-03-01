import time
import psutil
import requests
import json

# Load game name from config.json
CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

config = load_config()
GAME_NAME = config.get("game_name", "Minecraft")
HEROKU_URL = "https://game-approval-app-f9faeb466ffb.herokuapp.com/game-started"
HEROKU_CHECK_URL = "https://game-approval-app-f9faeb466ffb.herokuapp.com/check-approval"

def is_game_running(game_name):
    """Check if the game process is running"""
    for process in psutil.process_iter(attrs=['name']):
        if process.info['name'] and game_name.lower() in process.info['name'].lower():
            return True
    return False

def notify_heroku():
    """Send a request to Heroku when the game starts"""
    try:
        response = requests.post(HEROKU_URL)
        if response.status_code == 200:
            print(f"✅ Game '{GAME_NAME}' detected. Notification sent to Heroku.")
        else:
            print(f"❌ Failed to notify Heroku. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"❌ Error: {e}")

def check_approval():
    """Check if game is approved or denied"""
    try:
        response = requests.get(HEROKU_CHECK_URL)
        status = response.json().get("status", "pending")
        return status
    except requests.RequestException as e:
        print(f"❌ Error checking approval: {e}")
        return "pending"

def force_close_game(game_name):
    """Kill the game if not approved"""
    for process in psutil.process_iter(attrs=['name', 'pid']):
        if process.info['name'] and game_name.lower() in process.info['name'].lower():
            print(f"⛔ Closing '{game_name}' as it was denied.")
            subprocess.call(["kill", "-9", str(process.info['pid'])])

# Main loop to check for the game
print(f"🎮 Monitoring '{GAME_NAME}' on this Mac...")
game_was_running = False
game_was_notified = False  # Track if notification has been sent
game_approved = False  # Track if the game has been approved or denied

while True:
    if is_game_running(GAME_NAME):
        if not game_was_running:
            if not game_was_notified:  # Only notify if it hasn't been notified yet
                notify_heroku()  # Send notification to Slack
                game_was_notified = True  # Mark notification as sent
            game_was_running = True
        
        approval_status = check_approval()
        
        # If game is denied, close it
        if approval_status == "denied":
            force_close_game(GAME_NAME)
        # If game is approved, stop further checks (if desired)
        elif approval_status == "approved":
            game_approved = True
            print(f"✅ Game '{GAME_NAME}' is approved. No further checks needed.")
    
    else:
        if game_was_running:  # Game has just stopped
            game_was_notified = False  # Reset notification status
        game_was_running = False

    # Exit loop if the game is approved
    if game_approved:
        break
	
	print(f"🎮 Monitoring '{GAME_NAME}' on this Mac...")
game_was_running = False
game_was_notified = False  # Track if notification has been sent
game_approved = False  # Track if the game has been approved or denied

while True:
    if is_game_running(GAME_NAME):
        if not game_was_running:
            if not game_was_notified:  # Only notify if it hasn't been notified yet
                notify_heroku()  # Send notification to Slack
                game_was_notified = True  # Mark notification as sent
            game_was_running = True
        
        approval_status = check_approval()
        
        # If game is denied, close it
        if approval_status == "denied":
            force_close_game(GAME_NAME)
        # If game is approved, stop further checks (if desired)
        elif approval_status == "approved":
            game_approved = True
            print(f"✅ Game '{GAME_NAME}' is approved. No further checks needed.")
    
    else:
        if game_was_running:  # Game has just stopped
            game_was_notified = False  # Reset notification status
        game_was_running = False

    # Exit loop if the game is approved
    if game_approved:
        break

	time.sleep(10) # check for every 10 secs