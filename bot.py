import logging
import os
from telethon import TelegramClient, events, Button
from flask import Flask
from threading import Thread

# --- RENDER PORT FIX (FLASK) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running Successfully!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- CONFIGURATION ---
API_ID = 34135757
API_HASH = 'd3d5548fe0d98eb1fb793c2c37c9e5c8'
BOT_TOKEN = '8311404972:AAGuamaLW23YX2YBRHaQvrDO6VuivyPBdFo'
LOG_GROUP = -1003867805165  # Make sure this ID is correct
OWNER_ID = 8482447535
START_IMG = 'https://graph.org/file/3e0a6b443746a0e015d72-c32a268e5c7ec2feb4.jpg'

logging.basicConfig(level=logging.INFO)

# client initialize
client = TelegramClient('edit_guard', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# --- BUTTONS ---
MAIN_BUTTONS = [
    [
        Button.url("📢 Updates", "https://t.me/radhesupport"),
        Button.url("🎧 Support", "https://t.me/+PKYLDIEYiTljMzMx")
    ],
    [Button.url("👤 Owner", "https://t.me/XenoEmpir")]
]

# --- START COMMAND ---
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    user = await event.get_sender()
    caption = (
        "✨ **Welcome to Edit Guard Bot** ✨\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🛡️ **Main Groups mein edited messages ko detect karta hoon.**\n"
        "🚀 **Click /help for more info!**"
    )
    await event.reply(caption, file=START_IMG, buttons=MAIN_BUTTONS)
    
    # --- LOG GROUP MESSAGE (START) ---
    try:
        log_msg = f"👤 **New User Started Bot**\n\n**Name:** {user.first_name}\n**ID:** `{user.id}`"
        await client.send_message(LOG_GROUP, log_msg)
    except Exception as e:
        print(f"Log Error: {e}")

# --- EDIT DETECTION LOGIC ---
@client.on(events.MessageEdited)
async def edit_handler(event):
    if event.is_private:
        return
    
    try:
        chat = await event.get_chat()
        user = await event.get_sender()
        
        # Telethon me edited message ka content 'event.message.message' se milta hai
        new_msg = event.message.message 
        
        log_text = (
            "🛡️ **EDIT DETECTED** 🛡️\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👥 **Group:** `{chat.title}`\n"
            f"👤 **User:** [{user.first_name}](tg://user?id={user.id})\n"
            f"🆔 **User ID:** `{user.id}`\n\n"
            f"📝 **New/Edited Message:**\n`{new_msg}`\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━"
        )
        await client.send_message(LOG_GROUP, log_text)
    except Exception as e:
        print(f"Edit Handler Error: {e}")

# --- BOT INITIATION ---
if __name__ == "__main__":
    keep_alive()
    print("✅ Bot is Starting...")
    client.run_until_disconnected()
