import os
import asyncio
from telethon import TelegramClient, events, Button
from flask import Flask
from threading import Thread

# --- CONFIGURATIONS ---
API_ID = 34135757
API_HASH = 'd3d5548fe0d98eb1fb793c2c37c9e5c8'
BOT_TOKEN = '8311404972:AAG99KZLFFArJ8N_bh1X4tdcZPf6nNv2S2Q'
OWNER_ID = 8482447535
LOG_CHAT_ID = -1003867805165
START_IMG = 'https://graph.org/file/3e0a6b443746a0e015d72-c32a268e5c7ec2feb4.jpg'

# User tracking (Temporary - Reset on restart)
USERS = set()

# --- FLASK SERVER (Render Keep-Alive) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"
def run(): app.run(host='0.0.0.0', port=8080)

# --- BOT CLIENT ---
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# --- BUTTONS ---
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

# --- START COMMAND ---
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    if not event.is_private: return # Groups mein respond nahi karega
    USERS.add(event.sender_id)
    
    welcome_text = (
        "✨ **Wᴇʟᴄᴏᴍᴇ Tᴏ Eᴅɪᴛ Gᴜᴀʀᴅ Bᴏᴛ** ✨\n\n"
        "🛡️ Main aapke group ke edited messages ko track karke unhe log group mein bhejta hoon.\n\n"
        "🚀 **Sᴛᴀᴛᴜs:** Online & Active\n"
        "👤 **Oᴡɴᴇʀ:** [Xeno](tg://user?id=8482447535)\n\n"
        "Neeche diye gaye buttons use karein 👇"
    )
    await bot.send_file(event.chat_id, START_IMG, caption=welcome_text, buttons=MAIN_BUTTONS)

# --- HELP & GUIDE ---
@bot.on(events.NewMessage(pattern='/help'))
async def help_cmd(event):
    await event.reply("❓ **Hᴇʟᴘ Mᴇɴᴜ**\n\n• `/start` - Restart bot\n• `/help` - Show this menu\n• `/guide` - How to use\n• `/broadcast` - Owner only")

@bot.on(events.NewMessage(pattern='/guide'))
async def guide_cmd(event):
    await event.reply("📖 **Sᴇᴛᴜᴘ Gᴜɪᴅᴇ**\n\n1. Bot ko group mein add karein.\n2. Admin banayein.\n3. Ye automatic edited messages detect karega.")

# --- BROADCAST ---
@bot.on(events.NewMessage(pattern='/broadcast'))
async def broadcast(event):
    if event.sender_id != OWNER_ID:
        return await event.reply("❌ Only Owner can use this!")
    if not event.reply_to_msg_id:
        return await event.reply("Usage: Reply to a message with `/broadcast`")

    msg = await event.get_reply_message()
    count = 0
    progress = await event.reply("🚀 Sending...")

    for user in USERS:
        try:
            await bot.send_message(user, msg)
            count += 1
        except: pass
    
    await progress.edit(f"✅ **Broadcast Done!**\nTotal: `{count}` users.")

# --- CALLBACK (Buttons) ---
@bot.on(events.CallbackQuery)
async def callback(event):
    if event.data == b"help": await help_cmd(event)
    elif event.data == b"guide": await guide_cmd(event)

# --- EDIT GUARD LOGIC ---
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
    except: pass

# --- START ---
if __name__ == '__main__':
    Thread(target=run).start()
    print("Bot is alive!")
    bot.run_until_disconnected()
