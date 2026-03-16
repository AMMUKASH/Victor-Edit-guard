import logging
import os
import asyncio
from telethon import TelegramClient, events, Button, types
from flask import Flask
from threading import Thread

# --- RENDER/HEROKU PORT FIX ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"

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

# Memory me users save karne ke liye
users_list = set()

# --- HELPER LOG ---
async def send_log(text):
    try:
        await client.send_message(LOG_GROUP, text, link_preview=False)
    except: pass

# --- UI COMPONENTS ---
START_TEXT = (
    "✨ **𝐄𝐃𝐈𝐓 𝐆𝐔𝐀𝐑𝐃 𝐁𝐎𝐓** ✨\n\n"
    "🛡️ **𝐒𝐭𝐚𝐭𝐮𝐬:** `𝐀𝐜𝐭𝐢𝐯𝐞`\n"
    "💡 **𝐅𝐮𝐧𝐜𝐭𝐢𝐨𝐧:** `𝐀𝐮𝐭𝐨-𝐃𝐞𝐥𝐞𝐭𝐞 𝐄𝐝𝐢𝐭𝐞𝐝 𝐌𝐬𝐠`\n\n"
    "🚀 **𝐀𝐝𝐦𝐢𝐧𝐬, 𝐎𝐰𝐧𝐞𝐫𝐬, 𝐚𝐧𝐝 𝐀𝐧𝐨𝐧𝐲𝐦𝐨𝐮𝐬 𝐮𝐬𝐞𝐫𝐬—𝐧𝐨 𝐨𝐧𝐞 𝐜𝐚𝐧 𝐞𝐝𝐢𝐭 𝐦𝐞𝐬𝐬𝐚𝐠𝐞𝐬 𝐡𝐞𝐫𝐞!**"
)

START_BTNS = [
    [Button.inline("📖 𝐇𝐞𝐥𝐩 & 𝐆𝐮𝐢𝐝𝐞", b"help_menu")],
    [Button.url("❂ 𝐔𝐩𝐝𝐚𝐭𝐞 ❂", "https://t.me/radhesupport"), Button.url("👤 𝐎𝐰𝐧𝐞𝐫", "https://t.me/XenoEmpir")]
]

# --- START COMMAND ---
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    if event.is_private:
        users_list.add(event.sender_id)
    await event.reply(START_TEXT, file=START_IMG, buttons=START_BTNS)
    await send_log(f"👤 #𝐒𝐭𝐚𝐫𝐭\n**𝐔𝐬𝐞𝐫:** `{event.sender_id}`")

# --- CALLBACK (HELP MENU) ---
@client.on(events.CallbackQuery)
async def callback(event):
    if event.data == b"help_menu":
        help_text = (
            "📖 **𝐁𝐎𝐓 𝐇𝐄𝐋𝐏 & 𝐆𝐔𝐈𝐃𝐄**\n\n"
            "𝟏. **𝐀𝐝𝐝 𝐌𝐞:** 𝐀𝐝𝐝 𝐭𝐡𝐢𝐬 𝐛𝐨𝐭 𝐭𝐨 𝐲𝐨𝐮𝐫 𝐠𝐫𝐨𝐮𝐩.\n"
            "𝟐. **𝐏𝐫𝐨𝐦𝐨𝐭𝐞:** 𝐌𝐚𝐤𝐞 𝐦𝐞 𝐚𝐝𝐦𝐢𝐧 𝐰𝐢𝐭𝐡 '𝐃𝐞𝐥𝐞𝐭𝐞 𝐌𝐞𝐬𝐬𝐚𝐠𝐞𝐬' 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧.\n"
            "𝟑. **𝐖𝐨𝐫𝐤𝐢𝐧𝐠:** 𝐈 𝐰𝐢𝐥𝐥 𝐚𝐮𝐭𝐨-𝐝𝐞𝐥𝐞𝐭𝐞 𝐚𝐧𝐲 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐭𝐡𝐚𝐭 𝐠𝐞𝐭𝐬 𝐞𝐝𝐢𝐭𝐞𝐝.\n\n"
            "🛠️ **𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:**\n"
            "• `/start` - 𝐑𝐞𝐬𝐭𝐚𝐫𝐭 𝐭𝐡𝐞 𝐛𝐨𝐭.\n"
            "• `/broadcast` - (𝐎𝐰𝐧𝐞𝐫 𝐎𝐧𝐥𝐲) 𝐒𝐞𝐧𝐝 𝐦𝐬𝐠 𝐭𝐨 𝐚𝐥𝐥.\n\n"
            "🛡️ **𝐍𝐨𝐭𝐞:** 𝐄𝐯𝐞𝐧 𝐀𝐧𝐨𝐧𝐲𝐦𝐨𝐮𝐬 𝐀𝐝𝐦𝐢𝐧𝐬 𝐜𝐚𝐧'𝐭 𝐛𝐲𝐩𝐚𝐬𝐬 𝐭𝐡𝐢𝐬!"
        )
        await event.edit(help_text, buttons=[Button.inline("⬅️ 𝐁𝐚𝐜𝐤", b"back_start")])
    elif event.data == b"back_start":
        await event.edit(START_TEXT, buttons=START_BTNS)

# --- EDIT GUARD (ALL USERS) ---
@client.on(events.MessageEdited)
async def edit_handler(event):
    if event.is_private: return
    try:
        chat = await event.get_chat()
        sender = await event.get_sender()
        
        # Anonymous admin/Owner logic
        if isinstance(sender, types.Channel):
            sender_mention = "𝐀𝐧𝐨𝐧𝐲𝐦𝐨𝐮𝐬 𝐀𝐝𝐦𝐢𝐧 🎭"
        elif sender:
            sender_mention = f"[{sender.first_name}](tg://user?id={sender.id})"
        else:
            sender_mention = "𝐔𝐧𝐤𝐧𝐨𝐰𝐧 𝐔𝐬𝐞𝐫"

        msg_text = event.message.message or "Media Content"

        # 1. Delete message
        await event.delete()
        
        # 2. Notification (No Image)
        del_btns = [[Button.url("❂ 𝐔𝐩𝐝𝐚𝐭𝐞 ❂", "https://t.me/radhesupport"), 
                     Button.url("➕ 𝐀𝐝𝐝 𝐌𝐞 ➕", "https://t.me/EdiitGuardbot?startgroup=true")]]
        
        await event.respond(
            f"🛡️ **𝐄𝐃𝐈𝐓 𝐃𝐄𝐓𝐄𝐂𝐓𝐄𝐃 & 𝐃𝐄𝐋𝐄𝐓𝐄𝐃**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 **𝐔𝐬𝐞𝐫:** {sender_mention}\n"
            f"🚫 **𝐀𝐜𝐭𝐢𝐨𝐧:** `𝐌𝐞𝐬𝐬𝐚𝐠𝐞 𝐄𝐝𝐢𝐭 𝐏𝐫𝐨𝐡𝐢𝐛𝐢𝐭𝐞𝐝`\n"
            f"━━━━━━━━━━━━━━━━━━━━", 
            buttons=del_btns
        )
        
        # 3. Log Report
        log_text = (
            "🚀 #Edit_Event\n"
            f"👥 **Group:** `{chat.title}`\n"
            f"👤 **User:** {sender_name}\n"
            f"📝 **Msg:** `{msg_text}`"
        )
        await send_log(log_text)

# --- ADVANCED BROADCAST (LINKS & MEDIA) ---
@client.on(events.NewMessage(pattern='/broadcast'))
async def broadcast(event):
    if event.sender_id != OWNER_ID: return
    reply = await event.get_reply_message()
    if not reply: return await event.reply("❗ **𝐏𝐥𝐞𝐚𝐬𝐞 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 (𝐥𝐢𝐧𝐤, 𝐢𝐦𝐠, 𝐨𝐫 𝐭𝐞𝐱𝐭) 𝐭𝐨 𝐛𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭.**")
    
    status = await event.reply("📡 **𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭𝐢𝐧𝐠...**")
    count = 0
    for uid in list(users_list):
        try:
            # Full copy broadcast
            await client.send_message(uid, reply)
            count += 1
            await asyncio.sleep(0.3)
        except: pass
    await status.edit(f"✅ **𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭 𝐃𝐨𝐧𝐞!**\n\n✨ **𝐒𝐞𝐧𝐭 𝐭𝐨:** `{count}` 𝐮𝐬𝐞𝐫𝐬.")

if __name__ == "__main__":
    keep_alive()
    print("Xeno Edit Guard is active...")
    client.run_until_disconnected()
