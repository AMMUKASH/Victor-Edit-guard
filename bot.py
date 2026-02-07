import logging
import os
import asyncio
from telethon import TelegramClient, events, Button, types
from flask import Flask
from threading import Thread

# --- RENDER PORT FIX (Flask Server) ---
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
warns = {} # User warnings track karne ke liye

# --- BUTTONS ---
MAIN_BUTTONS = [
    [
        Button.url("❂ 𝐔𝐩𝐝𝐚𝐭𝐞 ❂", "https://t.me/radhesupport"),
        Button.url("❂ 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 ❂", "https://t.me/+PKYLDIEYiTljMzMx")
    ],
    [Button.inline("📖 𝖧𝖾𝗅𝗉 𝖬𝖾𝗇𝗎", b"help_menu"), Button.url("👤 𝖮𝗐𝗇𝖾𝗋", "https://t.me/XenoEmpir")]
]

# --- START COMMAND ---
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    users_list.add(event.sender_id)
    user = await event.get_sender()
    
    caption = (
        "╔══════════════════════╗\n"
        "      ✨ **𝖤𝖣𝖨𝖳 𝖦𝖴𝖠𝖱𝖣 𝖡𝖮𝖳** ✨\n"
        "╚══════════════════════╝\n\n"
        f"👋 **𝖧𝖾𝗅𝗅𝗈** [{user.first_name}](tg://user?id={user.id}) !\n\n"
        "🛡️ **𝖨 𝖺𝗆 𝖺 𝗉𝗈𝗐𝖾𝗋𝖿𝗎𝗅 𝖬𝖾𝗌𝗌𝖺𝗀𝖾 𝖤𝖽𝗂𝗍 𝖣𝖾𝗍𝖾𝖼𝗍𝗈𝗋.**\n"
        "💡 **𝖨 𝗐𝗂𝗅𝗅 𝗅𝗈𝗀 𝖾𝗏𝖾𝗋𝗒 𝖾𝖽𝗂𝗍𝖾𝖽 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗂𝗇 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉𝗌.**\n\n"
        "🚀 **𝖯𝗋𝖾𝗌𝗌 𝗍𝗁𝖾 𝖻𝗎𝗍𝗍𝗈𝗇 𝖻𝖾𝗅𝗈𝗐 𝖿𝗈𝗋 𝖬𝗈𝗋𝖾 𝖨𝗇𝖿𝗈!**\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    await event.reply(caption, file=START_IMG, buttons=MAIN_BUTTONS)

# --- EDIT GUARD WITH WARNINGS & LOGS ---
@client.on(events.MessageEdited)
async def edit_handler(event):
    if event.is_private: return
    try:
        chat = await event.get_chat()
        user = await event.get_sender()
        msg_text = event.message.message or "Media/Other"
        group_link = f"https://t.me/{chat.username}" if chat.username else "Private Group"
        
        # Warning Logic
        user_id = user.id
        warns[user_id] = warns.get(user_id, 0) + 1
        current_warns = warns[user_id]

        # 1. Delete message in group
        await event.delete()
        
        # 2. Group Notification (Image Style)
        del_buttons = [
            [
                Button.url("❂ 𝐔𝐩𝐝𝐚𝐭𝐞 ❂", "https://t.me/radhesupport"),
                Button.url("❂ 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 ❂", "https://t.me/+PKYLDIEYiTljMzMx")
            ],
            [Button.url("♻️ 𝐀𝐝𝐝 𝐌𝐞 𝐈𝐧 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 ♻️", "https://t.me/EdiitGuardbot?startgroup=true")]
        ]
        
        del_caption = (
            "🛡️ **𝖤𝖣𝖨𝖳 𝖣𝖤𝖳𝖤𝖢𝖳𝖤𝖣 & 𝖣𝖤𝖫𝖤𝖳𝖤𝖣**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 **𝖴𝗌𝖾𝗋:** [{user.first_name}](tg://user?id={user.id})\n"
            "🚫 **𝖵𝗂𝗈𝗅𝖺𝗍𝗂𝗈𝗇:** `𝖬𝖾𝗌𝗌𝖺𝗀𝖾 𝖠𝖻𝗎𝗌𝖾 / 𝖤𝖽𝗂𝗍`\n"
            f"⚠️ **𝖶𝖺𝗋𝗇𝗂𝗇𝗀:** `{current_warns}/3`\n"
            "━━━━━━━━━━━━━━━━━━━━"
        )
        await event.respond(del_caption, file=START_IMG, buttons=del_buttons)

        # 3. Log Group Report (Full Details)
        log_text = (
            "🛡️ **𝖤𝖣𝖨𝖳 𝖣𝖤𝖳𝖤𝖢𝖳𝖤𝖣 & 𝖣𝖤𝖫𝖤𝖳𝖤𝖣**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"👥 **𝖦𝗋𝗈𝗎𝗉 𝖭𝖺𝗆𝖾:** `{chat.title}`\n"
            f"🆔 **𝖦𝗋𝗈𝗎𝗉 𝖨𝖣:** `{chat.id}`\n"
            f"🔗 **𝖦𝗋𝗈𝗎𝗉 𝖫𝗂𝗇𝗄:** {group_link}\n"
            "────────────────────\n"
            f"👤 **𝖴𝗌𝖾𝗋:** [{user.first_name}](tg://user?id={user.id})\n"
            f"🆔 **𝖴𝗌𝖾𝗋 𝖨𝖣:** `{user.id}`\n"
            f"📝 **𝖤𝖽𝗂𝗍𝖾𝖽 𝖬𝗌𝗀:** `{msg_text}`\n"
            f"⚠️ **𝖱𝖾𝖺𝗌𝗈𝗇:** `𝖤𝖽𝗂𝗍 𝖦𝗎𝖺𝗋𝖽 𝖵𝗂𝗈𝗅𝖺𝗍𝗂𝗈𝗇`\n"
            "━━━━━━━━━━━━━━━━━━━━"
        )
        await client.send_message(LOG_GROUP, log_text)

        # Action if 3 warns reached
        if current_warns >= 3:
            await event.respond(f"🚫 [{user.first_name}](tg://user?id={user.id}) has reached 3/3 warnings and should be restricted.")
            warns[user_id] = 0 # Reset after action

    except: pass

# --- BROADCAST & HELP ---
@client.on(events.NewMessage(pattern='/broadcast'))
async def broadcast(event):
    if event.sender_id != OWNER_ID: return
    reply = await event.get_reply_message()
    if not reply: return await event.reply("Reply to a message!")
    msg = await event.reply("🚀 Sending...")
    count = 0
    for user_id in list(users_list):
        try:
            await client.send_message(user_id, reply)
            count += 1
            await asyncio.sleep(0.3)
        except: pass
    await msg.edit(f"✅ Sent to `{count}` users.")

if __name__ == "__main__":
    keep_alive()
    print("Xeno Edit Guard is running...")
    client.run_until_disconnected()
