import os
import asyncio
from telethon import TelegramClient, events, Button
from flask import Flask
from threading import Thread

# --- CONFIGURATIONS ---
API_ID = 34135757
API_HASH = 'd3d5548fe0d98eb1fb793c2c37c9e5c8'
BOT_TOKEN = '8311404972:AAFCmf7WIO8-PeVzz5G6oYn5F8JvyV_vTho'
OWNER_ID = 8482447535
LOG_CHAT_ID = -1003867805165
START_IMG = 'https://graph.org/file/3e0a6b443746a0e015d72-c32a268e5c7ec2feb4.jpg'

# User tracking for Broadcast (Simple list)
USERS = set()

# --- FLASK SERVER ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"
def run(): app.run(host='0.0.0.0', port=8080)

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# --- KEYBOARDS ---
MAIN_BUTTONS = [
    [
        Button.url("📢 Updates", "https://t.me/radhesupport"),
        Button.url("👥 Support", "https://t.me/+PKYLDIEYiTljMzMx")
    ],
    [
        Button.inline("📜 Help", data="help"),
        Button.inline("📖 Guide", data="guide")
    ],
    [Button.url("👨‍💻 Developer", "https://t.me/XenoEmpir")]
]

# --- COMMANDS ---

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    USERS.add(event.sender_id)
    text = (
        "✨ **Wᴇʟᴄᴏᴍᴇ Tᴏ Eᴅɪᴛ Gᴜᴀʀᴅ Bᴏᴛ** ✨\n\n"
        "🛡️ Main aapke group ke edited messages ko track karta hoon.\n\n"
        "🚀 **Sᴛᴀᴛᴜs:** Online & Active\n"
        "👤 **Oᴡɴᴇʀ:** [Xeno](tg://user?id=8482447535)\n\n"
        "Neeche diye gaye buttons se help lein 👇"
    )
    await bot.send_file(event.chat_id, START_IMG, caption=text, buttons=MAIN_BUTTONS)

@bot.on(events.NewMessage(pattern='/help'))
async def help_cmd(event):
    help_text = (
        "❓ **Hᴇʟᴘ Mᴇɴᴜ**\n\n"
        "• `/start` - Bot ko shuru karein.\n"
        "• `/help` - Ye menu dekhne ke liye.\n"
        "• `/guide` - Bot kaise setup karein.\n"
        "• `/broadcast` - Sirf Owner ke liye."
    )
    await event.reply(help_text)

@bot.on(events.NewMessage(pattern='/guide'))
async def guide_cmd(event):
    guide_text = (
        "📖 **Sᴇᴛᴜᴘ Gᴜɪᴅᴇ**\n\n"
        "1️⃣ Bot ko apne group mein add karein.\n"
        "2️⃣ Bot ko **Admin** banayein aur 'Delete Message' ki permission dein (optional).\n"
        "3️⃣ Bas! Ab koi bhi message edit hoga toh main use detect kar lunga."
    )
    await event.reply(guide_text)

# --- BROADCAST SYSTEM ---
@bot.on(events.NewMessage(pattern='/broadcast'))
async def broadcast(event):
    if event.sender_id != OWNER_ID:
        return await event.reply("❌ Sirf Owner hi broadcast kar sakta hai!")
    
    if not event.reply_to_msg_id:
        return await event.reply("Usage: `/broadcast` (kisi message ko reply karke)")

    msg = await event.get_reply_message()
    count = 0
    status = await event.reply("🚀 Broadcast shuru ho raha hai...")

    for user in USERS:
        try:
            await bot.send_message(user, msg)
            count += 1
        except:
            pass
    
    await status.edit(f"✅ **Broadcast Done!**\nSent to: `{count}` users.")

# --- CALLBACK QUERIES (Buttons) ---
@bot.on(events.CallbackQuery)
async def callback(event):
    if event.data == b"help":
        await event.answer("Opening Help...", alert=True)
        await help_cmd(event)
    elif event.data == b"guide":
        await event.answer("Opening Guide...", alert=True)
        await guide_cmd(event)

# --- EDIT DETECTION ---
@bot.on(events.MessageEdited)
async def edit_handler(event):
    if event.is_private: return
    try:
        user = await event.get_sender()
        chat = await event.get_chat()
        
        log_text = (
            "🚀 **ᴇᴅɪᴛ ᴅᴇᴛᴇᴄᴛᴇᴅ**\n\n"
            f"👤 **Usᴇʀ:** [{user.first_name}](tg://user?id={user.id})\n"
            f"🏛️ **Gʀᴏᴜᴘ:** {chat.title}\n"
            f"🖋️ **ɴᴇᴡ:** `{event.text}`"
        )
        await bot.send_message(LOG_CHAT_ID, log_text)
        await event.reply(f"⚠️ **Eᴅɪᴛ Aʟᴇʀᴛ!** [{user.first_name}](tg://user?id={user.id}), edit mat karo!")
    except:
        pass

if __name__ == '__main__':
    Thread(target=run).start()
    bot.run_until_disconnected()
