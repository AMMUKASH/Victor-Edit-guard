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

users_list = set()

# --- BUTTONS ---
MAIN_BUTTONS = [
    [
        Button.url("📢 𝖴𝗉𝖽𝖺𝗍𝖾𝗌", "https://t.me/radhesupport"),
        Button.url("🎧 𝖲𝗎𝗉𝗉𝗈𝗋𝗍", "https://t.me/+PKYLDIEYiTljMzMx")
    ],
    [Button.inline("📖 𝖧𝖾𝗅𝗉 𝖬𝖾𝗇𝗎", b"help_menu"), Button.url("👤 𝖮𝗐𝗇𝖾𝗋", "https://t.me/XenoEmpir")]
]

# --- START COMMAND (STYLISH CAPTION) ---
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    users_list.add(event.sender_id)
    user = await event.get_sender()
    
    # New Stylish Caption
    caption = (
        "╔══════════════════════╗\n"
        "      ✨ **𝖤𝖣𝖨𝖳 𝖦𝖴𝖠𝖱𝖣 𝖡𝖮𝖳** ✨\n"
        "╚══════════════════════╝\n\n"
        "👋 **𝖧𝖾𝗅𝗅𝗈** " + f"[{user.first_name}](tg://user?id={user.id})" + " !\n\n"
        "🛡️ **𝖨 𝖺𝗆 𝖺 𝗉𝗈𝗐𝖾𝗋𝖿𝗎𝗅 𝖬𝖾𝗌𝗌𝖺𝗀𝖾 𝖤𝖽𝗂𝗍 𝖣𝖾𝗍𝖾𝖼𝗍𝗈𝗋.**\n"
        "💡 **𝖨 𝗐𝗂𝗅𝗅 𝗅𝗈𝗀 𝖾𝗏𝖾𝗋𝗒 𝖾𝖽𝗂𝗍𝖾𝖽 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗂𝗇 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉𝗌.**\n\n"
        "🚀 **𝖯𝗋𝖾𝗌𝗌 𝗍𝗁𝖾 𝖻𝗎𝗍𝗍𝗈𝗇 𝖻𝖾𝗅𝗈𝗐 𝖿𝗈𝗋 𝖬𝗈𝗋𝖾 𝖨𝗇𝖿𝗈!**\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    await event.reply(caption, file=START_IMG, buttons=MAIN_BUTTONS)
    
    # Log Group Notification (Exact like your screenshot with Mention)
    try:
        log_text = (
            "𝖤𝖣𝖨𝖳 𝖦𝖴𝖠𝖱𝖣𝖨𝖠𝖭\n"
            f"👤 **𝖭𝖾𝗐 𝖴𝗌𝖾𝗋:** [{user.first_name}](tg://user?id={user.id})\n"
            f"🆔 **𝖨𝖣:** `{user.id}`"
        )
        await client.send_message(LOG_GROUP, log_text)
    except: pass

# --- HELP CALLBACK & COMMAND ---
@client.on(events.NewMessage(pattern='/help'))
@client.on(events.CallbackQuery(data=b"help_menu"))
async def help_handler(event):
    help_text = (
        "📖 **𝖤𝖽𝗂𝗍 𝖦𝗎𝖺𝗋𝖽 - 𝖧𝖾𝗅𝗉 𝖦𝗎𝗂𝖽𝖾**\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔹 **/𝗌𝗍𝖺𝗋𝗍** : 𝖳𝗈 𝗋𝖾𝗌𝗍𝖺𝗋𝗍 𝗍𝗁𝖾 𝖻𝗈𝗍.\n"
        "🔹 **/𝗁𝖾𝗅𝗉** : 𝖳𝗈 𝗀𝖾𝗍 𝗍𝗁𝗂𝗌 𝗆𝖾𝗇𝗎.\n"
        "🔹 **/𝖻𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍** : (𝖮𝗐𝗇𝖾𝗋 𝖮𝗇𝗅𝗒).\n\n"
        "⚠️ **𝖭𝗈𝗍𝖾:** 𝖬𝖺𝗄𝖾 𝗆𝖾 𝖠𝖽𝗆𝗂𝗇 𝗂𝗇 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉 𝗐𝗂𝗍𝗁 '𝖯𝗈𝗌𝗍 𝖬𝖾𝗌𝗌𝖺𝗀𝖾𝗌' 𝗉𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇!"
    )
    if isinstance(event, events.CallbackQuery.Event):
        await event.edit(help_text, buttons=[Button.inline("⬅️ 𝖡𝖺𝖼𝗄", b"start_back")])
    else:
        await event.reply(help_text)

@client.on(events.CallbackQuery(data=b"start_back"))
async def back_to_start(event):
    # Back to start UI logic
    user = await event.get_sender()
    caption = (
        "╔══════════════════════╗\n"
        "      ✨ **𝖤𝖣𝖨𝖳 𝖦𝖴𝖠𝖱𝖣 𝖡𝖮𝖳** ✨\n"
        "╚══════════════════════╝\n\n"
        "👋 **𝖧𝖾𝗅𝗅𝗈** " + f"[{user.first_name}](tg://user?id={user.id})" + " !\n\n"
        "🚀 **𝖨'𝗆 𝗋𝖾𝖺𝖽𝗒 𝗍𝗈 𝗀𝗎𝖺𝗋𝖽 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉𝗌.**"
    )
    await event.edit(caption, file=START_IMG, buttons=MAIN_BUTTONS)

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
    for user_id in list(users_list):
        try:
            await client.send_message(user_id, reply)
            count += 1
            await asyncio.sleep(0.3)
        except: pass
    
    await msg.edit(f"✅ **𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽!**\n\n📢 **𝖲𝖾𝗇𝗍 𝖳𝗈:** `{count}` 𝖴𝗌𝖾𝗋𝗌")

# --- EDIT DETECTION LOGIC (WITH MENTION) ---
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
            f"👤 **𝖴𝗌𝖾𝗋:** [{user.first_name}](tg://user?id={user.id})\n"
            f"🆔 **𝖨𝖣:** `{user.id}`\n\n"
            f"📝 **𝖭𝖾𝗐 𝖬𝖾𝗌𝗌𝖺𝗀𝖾:**\n`{new_msg}`\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━"
        )
        await client.send_message(LOG_GROUP, log_text)
    except: pass

if __name__ == "__main__":
    keep_alive()
    print("✅ Bot is Starting...")
    client.run_until_disconnected()
