"""
user amiit.singh is sending message to AI-Bot from there it is picked
and responded by python program:

message flow -
============
1. amiit.singh (user)
📝 sends a direct message in Slack → to AI-Bot
2. AI-Bot (bot app inside Slack)
Listens for incoming events via Socket Mode

3. Python Program (with Slack Bolt SDK)
Receives the event (e.g., message)

Logs it, processes it

Optionally replies back to Slack using say(...)

4. Slack shows bot reply to amiit.singh
e.g., “Hi <@amiit.singh>, you said: hello”




"""





import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv

load_dotenv()
# Set your tokens here
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
print(SLACK_BOT_TOKEN, SLACK_APP_TOKEN)


# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)


# Event: Message received in DM
@app.event("message")
def handle_dm_messages(event, say, context):
    channel_type = event.get("channel_type")
    user = event.get("user")
    text = event.get("text")

    # Only handle DMs and skip bot's own messages
    if channel_type == "im" and user and text:
        print(f"Received from {user}: {text}")
        say(f"Hi <@{user}>, you said: {text}")


# Start the bot
if __name__ == "__main__":
    print("🤖 Bot is running and listening via Socket Mode...")
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
