import logging
import os
import asyncio
from telethon import TelegramClient, events, Button
from flask import Flask
from threading import Thread

# --- RENDER PORT FIX ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Running Successfully!"

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
LOG_GROUP = -1003867805165 
OWNER_ID = 8482447535
START_IMG = 'https://graph.org/file/3e0a6b443746a0e015d72-c32a268e5c7ec2feb4.jpg'

logging.basicConfig(level=logging.INFO)
client = TelegramClient('edit_guard', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# --- DATABASE (Simple List for Broadcast) ---
# Note: Real bot ke liye Database (MongoDB/SQL) use karna chahiye.
users_list = set()

# --- BUTTONS ---
MAIN_BUTTONS = [
    [
        Button.url("📢 𝖴𝗉𝖽𝖺𝗍𝖾𝗌", "https://t.me/radhesupport"),
        Button.url("🎧 𝖲𝗎𝗉𝗉𝗈𝗋𝗍", "https://t.me/+PKYLDIEYiTljMzMx")
    ],
    [Button.inline("📖 𝖧𝖾𝗅𝗉 𝖬𝖾𝗇𝗎", b"help_menu"), Button.url("👤 𝖮𝗐𝗇𝖾𝗋", "https://t.me/XenoEmpir")]
]

# --- START COMMAND ---
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    users_list.add(event.sender_id)
    user = await event.get_sender()
    caption = (
        "✨ **𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝗍𝗈 𝖤𝖽𝗂𝗍 𝖦𝗎𝖺𝗋𝖽 𝖡𝗈𝗍** ✨\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🛡️ **𝖬𝖺𝗂𝗇 𝖦𝗋𝗈𝗎𝗉𝗌 𝗆𝖾𝗂𝗇 𝖾𝖽𝗂𝗍𝖾𝖽 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝗄𝗈 𝖽𝖾𝗍𝖾𝗀𝗍 𝗄𝖺𝗋𝗍𝖺 𝗁𝗈𝗈𝗇.**\n"
        "🚀 **𝖢𝗅𝗂𝖼𝗄 𝖻𝖾𝗅𝗈𝗐 𝖿𝗈𝗋 𝗆𝗈𝗋𝖾 𝗂𝗇𝖿𝗈!**"
    )
    await event.reply(caption, file=START_IMG, buttons=MAIN_BUTTONS)
    try:
        await client.send_message(LOG_GROUP, f"👤 **𝖭𝖾𝗐 𝖴𝗌𝖾𝗋:** {user.first_name}\n🆔 **𝖨𝖣:** `{user.id}`")
    except: pass

# --- HELP CALLBACK & COMMAND ---
@client.on(events.NewMessage(pattern='/help'))
@client.on(events.CallbackQuery(data=b"help_menu"))
async def help_handler(event):
    help_text = (
        "📖 **𝖤𝖽𝗂𝗍 𝖦𝗎𝖺𝗋𝖽 - 𝖧𝖾𝗅𝗉 𝖦𝗎𝗂𝖽𝖾**\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔹 **/𝗌𝗍𝖺𝗋𝗍** : 𝖳𝗈 𝖼𝗁𝖾𝖼𝗄 𝗂𝖿 𝖻𝗈𝗍 𝖺𝗅𝗂𝗏𝖾.\n"
        "🔹 **/𝗁𝖾𝗅𝗉** : 𝖳𝗈 𝗌𝖾𝖾 𝗍𝗁𝗂𝗌 𝗆𝖾𝗇𝗎.\n"
        "🔹 **/𝖻𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍** : (𝖮𝗐𝗇𝖾𝗋 𝖮𝗇𝗅𝗒).\n\n"
        "⚠️ **𝖭𝗈𝗍𝖾:** 𝖡𝗈𝗍 𝗆𝗎𝗌𝗍 𝖻𝖾 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉 𝗍𝗈 𝖽𝖾𝗍𝖾𝗀𝗍 𝖾𝖽𝗂𝗍𝗌!"
    )
    if isinstance(event, events.CallbackQuery.Event):
        await event.edit(help_text, buttons=[Button.inline("⬅️ 𝖡𝖺𝖼𝗄", b"start_back")])
    else:
        await event.reply(help_text)

@client.on(events.CallbackQuery(data=b"start_back"))
async def back_to_start(event):
    await event.edit(file=START_IMG, buttons=MAIN_BUTTONS)

# --- STYLISH BROADCAST COMMAND ---
@client.on(events.NewMessage(pattern='/broadcast'))
async def broadcast(event):
    if event.sender_id != OWNER_ID:
        return await event.reply("❌ **𝖲𝗂𝗋𝗿 𝖮𝗐𝗇𝖾𝗋 𝗁𝗂 𝗎𝗌𝖾 𝗄𝖺𝗋 𝗌𝖺𝗄𝗍𝖺 𝗁𝖺𝗂!**")
    
    reply = await event.get_reply_message()
    if not reply:
        return await event.reply("👉 **𝖬𝖾𝗌𝗌𝖺𝗀𝖾 𝗄𝗈 𝗋𝖾𝗉𝗅𝗒 𝗄𝖺𝗋𝗄𝖾 `/𝖻𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍` 𝗅𝗂𝗄𝗁𝖾𝗂𝗇.**")
    
    msg = await event.reply("🚀 **𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖲𝗍𝖺𝗋𝗍𝗂𝗇𝗀...**")
    count = 0
    for user_id in users_list:
        try:
            await client.send_message(user_id, reply)
            count += 1
            await asyncio.sleep(0.3) # Avoid FloodWait
        except: pass
    
    await msg.edit(f"✅ **𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽!**\n\n📢 **𝖲𝖾𝗇𝗍 𝖳𝗈:** `{count}` 𝖴𝗌𝖾𝗋𝗌")

# --- EDIT DETECTION ---
@client.on(events.MessageEdited)
async def edit_handler(event):
    if event.is_private: return
    try:
        chat = await event.get_chat()
        user = await event.get_sender()
        new_msg = event.message.message 
        
        log_text = (
            "🛡️ **𝖤𝖣𝖨𝖳 𝖣𝖤𝖳𝖤𝖢𝖳𝖤𝖣** 🛡️\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👥 **𝖦𝗋𝗈𝗎𝗉:** `{chat.title}`\n"
            f"👤 **𝖴𝗌𝖾𝗋:** [{user.first_name}](tg://user?id={user.id})\n\n"
            f"📝 **𝖬𝖾𝗌𝗌𝖺𝗀𝖾:**\n`{new_msg}`\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━"
        )
        await client.send_message(LOG_GROUP, log_text)
    except: pass

if __name__ == "__main__":
    keep_alive()
    print("✅ Bot is Starting...")
    client.run_until_disconnected()
