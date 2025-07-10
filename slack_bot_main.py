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
######################################################################
######################################################################

# Up to 10 threads will run in parallel, each handling one user message at a time.
# Thread Pool version of the Slack bot using concurrent.futures.ThreadPoolExecutor.
#
# This allows the bot to handle multiple user messages in parallel, ideal for:
#
# Slower logic (e.g., calling Mistral or external APIs)
#
# 100+ active users


from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

# Load environment variables
load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

# Check tokens
if not SLACK_BOT_TOKEN or not SLACK_APP_TOKEN:
    print("❌ Missing Slack tokens. Check your .env file.")
    exit(1)

# Initialize Slack App
app = App(token=SLACK_BOT_TOKEN)

# Create a thread pool executor
executor = ThreadPoolExecutor(max_workers=10)  # Adjust thread count as needed

# Message processor function
def process_message(event, say):
    try:
        user = event.get("user")
        text = event.get("text")
        channel_type = event.get("channel_type")

        if channel_type == "im" and user and text:
            print(f"📥 DM from {user}: {text}")
            say(f"Hi <@{user}>, you said: {text}")

    except Exception as e:
        print("⚠️ Error in message processor:", e)

# Event handler (sends task to thread pool)
@app.event("message")
def handle_message(event, say):
    executor.submit(process_message, event, say)

# Start the bot via Socket Mode
if __name__ == "__main__":
    print("🤖 Bot is running with ThreadPoolExecutor and listening via Socket Mode...")
    SocketModeHandler(app, SLACK_APP_TOKEN).start()





######################################################################
# this is one thread with one queue, if 10 message from 10 uses comes , they will be in que
# one thread will handle all the user message from que one by one.

# from queue import Queue
# from threading import Thread
# from slack_bolt import App
# from slack_bolt.adapter.socket_mode import SocketModeHandler
# import os
# from dotenv import load_dotenv
#
# # Load tokens from .env
# load_dotenv()
# SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
# SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
#
# # Check tokens
# if not SLACK_BOT_TOKEN or not SLACK_APP_TOKEN:
#     print("❌ Missing SLACK_BOT_TOKEN or SLACK_APP_TOKEN. Check your .env file.")
#     exit(1)
#
# # Initialize Slack App
# app = App(token=SLACK_BOT_TOKEN)
#
# # Create event queue and worker thread
# event_queue = Queue()
#
# def worker():
#     while True:
#         try:
#             event, say = event_queue.get()
#             user = event.get("user")
#             text = event.get("text")
#             channel_type = event.get("channel_type")
#
#             # Only handle direct messages (DMs)
#             if channel_type == "im" and user and text:
#                 print(f"📥 DM from {user}: {text}")
#                 say(f"Hi <@{user}>, you said: {text}")
#
#         except Exception as e:
#             print("⚠️ Error in worker thread:", e)
#         finally:
#             event_queue.task_done()
#
# # Start worker thread
# Thread(target=worker, daemon=True).start()
#
# # Slack event handler
# @app.event("message")
# def handle_message(event, say):
#     event_queue.put((event, say))
#
# # Start bot via Socket Mode
# if __name__ == "__main__":
#     print("🤖 Bot is running and listening via Socket Mode...")
#     SocketModeHandler(app, SLACK_APP_TOKEN).start()

##########################################################################









###########################################################################

# basic program : working
# from queue import Queue
# from threading import Thread
# from slack_bolt import App
# from slack_bolt.adapter.socket_mode import SocketModeHandler
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
# # Set your tokens here
# SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
# SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
# print(SLACK_BOT_TOKEN, SLACK_APP_TOKEN)
#
#
# # Initialize the Slack app
# app = App(token=SLACK_BOT_TOKEN)
#
# event_queue = Queue()
#
# def worker():
#     while True:
#         event, say = event_queue.get()
#         user = event["user"]
#         text = event["text"]
#         say(f"Hi <@{user}>, you said: {text}")
#         event_queue.task_done()
#
# Thread(target=worker, daemon=True).start()
#
# @app.event("message")
# def handle_message(event, say):
#     event_queue.put((event, say))
#
#
# # # Event: Message received in DM
# # @app.event("message")
# # def handle_dm_messages(event, say, context):
# #     channel_type = event.get("channel_type")
# #     user = event.get("user")
# #     text = event.get("text")
# #
# #     # Only handle DMs and skip bot's own messages
# #     if channel_type == "im" and user and text:
# #         print(f"Received from {user}: {text}")
# #         say(f"Hi <@{user}>, you said: {text}")
#
#
# # Start the bot
# if __name__ == "__main__":
#     print("🤖 Bot is running and listening via Socket Mode...")
#     SocketModeHandler(app, SLACK_APP_TOKEN).start()
