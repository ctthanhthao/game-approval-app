# Game Approval App

## 📌 Overview
Game Approval App is a parental control tool that detects when a game starts on a child's macOS device and sends a notification to Slack for approval. The parent can then approve or deny the request. If denied, the game is automatically closed.

## 🚀 Features
- Detects when a specific game starts on macOS.
- Sends an approval request to Slack.
- Parent can approve or deny directly from Slack.
- Prevents unauthorized game access by force-closing denied games.
- Uses **Heroku** to manage approval requests.

## 🛠️ Tech Stack
- **Python** (Flask, psutil, requests, slack_sdk)
- **Heroku** (for hosting the approval backend)
- **Slack API** (for sending and receiving approval requests)

---

## 📌 Installation Guide

### 1️⃣ Set Up the Backend on Heroku
#### **Step 1: Clone the Repository**
```bash
git clone https://github.com/ctthanhthao/game-approval-app.git
cd game-approval-app
```

#### **Step 2: Create a Heroku App**
```bash
heroku create game-approval-app
```

#### **Step 3: Set Environment Variables**
```bash
heroku config:set SLACK_TOKEN=your-slack-bot-token
heroku config:set SLACK_CHANNEL=your-slack-channel-id
```

#### **Step 4: Deploy to Heroku**
```bash
git add .
git commit -m "Initial commit"
git push heroku main
```

#### **Step 5: Restart the Heroku App**
```bash
heroku restart
```

---

### 2️⃣ Set Up the macOS Game Monitor
#### **Step 1: Install Dependencies**
```bash
pip install psutil requests
```

#### **Step 2: Configure the Game Name**
Edit `config.json`:
```json
{
  "game_name": "Minecraft"
}
```

#### **Step 3: Run the Monitor Script**
```bash
python3 monitor_game.py
```

#### **Step 4: (Optional) Run the Script on Startup**
To automatically start the game monitor when macOS boots up:
1. Open **Terminal** and run:
   ```bash
   crontab -e
   ```
2. Add this line at the end to run the script at startup:
   ```bash
   @reboot /usr/bin/python3 /path/to/monitor_game.py
   ```
3. Save and exit.

---

## 📌 How It Works
1. The **monitor script** runs on macOS and detects when the game starts.
2. It **sends a request to Heroku**, which notifies **Slack**.
3. Parent receives a **Slack message with Allow/Deny buttons**.
4. If **allowed**, the game runs normally.
5. If **denied**, the game **is force-closed**.

---

## 📌 API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/game-started` | POST | Notifies Slack when the game starts |
| `/slack-interaction` | POST | Handles Slack button responses |
| `/check-approval` | GET | Returns the approval status |

---

## 📌 Scale down or scale up web application
- stop a web app or if you're saving costs
```bash
heroku ps:scale web=0
```
- start web app
```bash
heroku ps:scale web=1
```

## 📌 Troubleshooting
**1️⃣ Game is not detected?**
- Ensure the **correct game name** is in `config.json`.
- Run `ps aux | grep GameName` to check the correct process name.

**2️⃣ Slack message not appearing?**
- Double-check **SLACK_TOKEN** and **SLACK_CHANNEL**.
- Run `heroku logs --tail` to check for errors.

**3️⃣ Game not closing when denied?**
- Ensure **psutil** is installed.
- Run `python3 monitor_game.py` in debug mode to see logs.

---

## 📌 Future Enhancements
- Add a web dashboard for manual approvals.
- Support multiple monitored games.
- Improve UI/UX for Slack messages.

---

## 📌 License
MIT License. Feel free to modify and use!
