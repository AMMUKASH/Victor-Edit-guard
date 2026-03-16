import logging
import os
import asyncio
from telethon import TelegramClient, events, Button, types
from flask import Flask
from threading import Thread

# --- RENDER/HEROKU PORT FIX ---
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

# Broadcast ke liye database (Set use kar rahe hain memory me)
users_list = set()

# --- LOGGING FUNCTION ---
async def send_log(text):
    try:
        await client.send_message(LOG_GROUP, text, link_preview=False)
    except: pass

# --- START COMMAND ---
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    if event.is_private:
        users_list.add(event.sender_id)
    
    user = await event.get_sender()
    caption = (
        "╔══════════════════════╗\n"
        "      ✨ **𝐄𝐃𝐈𝐓 𝐆𝐔𝐀𝐑𝐃 𝐁𝐎𝐓** ✨\n"
        "╚══════════════════════╝\n\n"
        f"👋 **𝐇𝐞𝐥𝐥𝐨** [{user.first_name}](tg://user?id={user.id}) !\n\n"
        "🛡️ **𝐈 𝐚𝐦 𝐚 𝐩𝐨𝐰𝐞𝐫𝐟𝐮𝐥 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 𝐄𝐝𝐢𝐭 𝐃𝐞𝐭𝐞𝐜𝐭𝐨𝐫.**\n"
        "💡 **𝐈 𝐰𝐢𝐥𝐥 𝐝𝐞𝐥𝐞𝐭𝐞 𝐞𝐯𝐞𝐫𝐲 𝐞𝐝𝐢𝐭𝐞𝐝 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐢𝐧 𝐲𝐨𝐮𝐫 𝐠𝐫𝐨𝐮𝐩𝐬.**\n\n"
        "🚀 **𝐏𝐫𝐞𝐬𝐬 𝐭𝐡𝐞 𝐛𝐮𝐭𝐭𝐨𝐧𝐬 𝐛𝐞𝐥𝐨𝐰 𝐟𝐨𝐫 𝐦𝐨𝐫𝐞!**\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    buttons = [
        [
            Button.url("❂ 𝐔𝐩𝐝𝐚𝐭𝐞 ❂", "https://t.me/radhesupport"),
            Button.url("❂ 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 ❂", "https://t.me/+PKYLDIEYiTljMzMx")
        ],
        [Button.url("👤 𝐎𝐰𝐧𝐞𝐫", "https://t.me/XenoEmpir")]
    ]
    await event.reply(caption, file=START_IMG, buttons=buttons)
    await send_log(f"👤 #𝐒𝐭𝐚𝐫𝐭\n**𝐔𝐬𝐞𝐫:** {user.first_name}\n**𝐈𝐃:** `{user.id}`")

# --- EDIT GUARD LOGIC ---
@client.on(events.MessageEdited)
async def edit_handler(event):
    if event.is_private: return
    try:
        chat = await event.get_chat()
        user = await event.get_sender()
        if not user: return
        
        msg_text = event.message.message or "Media/Other"
        
        # 1. Message Delete Karo
        await event.delete()
        
        # 2. Group Me Notification Bhejo Buttons Ke Sath
        del_buttons = [
            [
                Button.url("❂ 𝐔𝐩𝐝𝐚𝐭𝐞 ❂", "https://t.me/radhesupport"),
                Button.url("➕ 𝐀𝐝𝐝 𝐌𝐞 ➕", "https://t.me/EdiitGuardbot?startgroup=true")
            ]
        ]
        
        del_caption = (
            "🛡️ **𝐄𝐃𝐈𝐓 𝐃𝐄𝐓𝐄𝐂𝐓𝐄𝐃 & 𝐃𝐄𝐋𝐄𝐓𝐄𝐃**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 **𝐔𝐬𝐞𝐫:** [{user.first_name}](tg://user?id={user.id})\n"
            "🚫 **𝐀𝐜𝐭𝐢𝐨𝐧:** `𝐌𝐞𝐬𝐬𝐚𝐠𝐞 𝐄𝐝𝐢𝐭 𝐏𝐫𝐨𝐡𝐢𝐛𝐢𝐭𝐞𝐝`\n"
            "✨ **𝐒𝐭𝐚𝐭𝐮𝐬:** `𝐃𝐞𝐥𝐞𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲`\n"
            "━━━━━━━━━━━━━━━━━━━━"
        )
        await event.respond(del_caption, file=START_IMG, buttons=del_buttons)

        # 3. Log Group Report
        log_text = (
            "🚀 #𝐄𝐝𝐢𝐭_𝐄𝐯𝐞𝐧𝐭\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"👥 **𝐆𝐫𝐨𝐮𝐩:** `{chat.title}`\n"
            f"👤 **𝐔𝐬𝐞𝐫:** {user.first_name} (`{user.id}`)\n"
            f"📝 **𝐌𝐬𝐠:** `{msg_text}`\n"
            "━━━━━━━━━━━━━━━━━━━━"
        )
        await send_log(log_text)
    except: pass

# --- BROADCAST FEATURE ---
@client.on(events.NewMessage(pattern='/broadcast'))
async def broadcast(event):
    if event.sender_id != OWNER_ID:
        return await event.reply("❌ **𝐒𝐨𝐫𝐫𝐲, 𝐨𝐧𝐥𝐲 𝐎𝐰𝐧𝐞𝐫 𝐜𝐚𝐧 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬!**")
    
    reply = await event.get_reply_message()
    if not reply:
        return await event.reply("❗ **𝐏𝐥𝐞𝐚𝐬𝐞 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐭𝐨 𝐛𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭.**")
    
    status_msg = await event.reply("📡 **𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭 𝐢𝐧 𝐩𝐫𝐨𝐠𝐫𝐞𝐬𝐬...**")
    count = 0
    for user_id in list(users_list):
        try:
            await client.send_message(user_id, reply)
            count += 1
            await asyncio.sleep(0.2) # Avoid spam ban
        except: pass
    
    await status_msg.edit(f"✅ **𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭 𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞𝐝!**\n\n✨ **𝐒𝐞𝐧𝐭 𝐭𝐨:** `{count}` users.")
    await send_log(f"📢 #𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭\n**𝐎𝐰𝐧𝐞𝐫:** `{OWNER_ID}`\n**𝐒𝐞𝐧𝐭 𝐭𝐨:** `{count}` users.")

if __name__ == "__main__":
    keep_alive()
    print("Xeno Edit Guard is active...")
    client.run_until_disconnected()
