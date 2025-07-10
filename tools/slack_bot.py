import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

class SlackBot:
    def __init__(self):
        load_dotenv()
        self.bot_token = os.getenv("SLACK_BOT_TOKEN")
        self.app_token = os.getenv("SLACK_APP_TOKEN")

        if not self.bot_token or not self.app_token:
            raise ValueError("❌ Missing Slack tokens. Check your .env file.")

        self.app = App(token=self.bot_token)
        self.executor = ThreadPoolExecutor(max_workers=10)

        self.setup_events()

    def setup_events(self):
        @self.app.event("message")
        def handle_message(event, say):
            self.executor.submit(self.process_message, event, say)

    def process_message(self, event, say):
        try:
            user = event.get("user")
            text = event.get("text")
            channel_type = event.get("channel_type")

            if channel_type == "im" and user and text:
                print(f"📥 DM from {user}: {text}")
                say(f"Hi <@{user}>, you said: {text}")
        except Exception as e:
            print("⚠️ Error in process_message:", e)

    def run(self):
        print("🤖 SlackBot is running with ThreadPoolExecutor via Socket Mode...")
        SocketModeHandler(self.app, self.app_token).start()
