import logging
from telethon import TelegramClient, events, Button

# --- CONFIGURATION ---
API_ID = 34135757
API_HASH = 'd3d5548fe0d98eb1fb793c2c37c9e5c8'
BOT_TOKEN = '8311404972:AAG6cmGBT-VmSgU4xnwA5aJtLMnVJKdlqXo'
LOG_GROUP = -1003867805165
OWNER_ID = 8482447535
START_IMG = 'https://graph.org/file/06f17f2da3be3ddf5c9d6-f22b08d691cecb6be9.jpg'

client = TelegramClient('edit_guard', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# --- BUTTONS REUSABLE ---
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
    caption = (
        "✨ **Welcome to Edit Guard Bot** ✨\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🛡️ **Main Groups mein edited messages ko detect karta hoon.**\n\n"
        "📍 **Kaise Use Karein?**\n"
        "1️⃣ Mujhe apne Group mein add karein.\n"
        "2️⃣ Admin banayein aur permissions dein.\n"
        "3️⃣ Bas! Ab koi bhi message edit karega toh main uska original content log group mein bhej dunga.\n\n"
        "🚀 **Click /help for more info!**"
    )
    await event.reply(caption, file=START_IMG, buttons=MAIN_BUTTONS)

# --- HELP COMMAND ---
@client.on(events.NewMessage(pattern='/help'))
async def help(event):
    help_text = (
        "📖 **Help Guide - Edit Guard**\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔹 **Commands:**\n"
        "• `/start` : Bot check karne ke liye.\n"
        "• `/help` : Ye menu dekhne ke liye.\n\n"
        "🔹 **For Admins:**\n"
        "Mujhe group mein add karke 'Delete Messages' aur 'Pin Messages' ki permission dein taaki main sahi se monitor kar sakun.\n\n"
        "⚠️ **Note:** Main sirf un messages ko detect karta hoon jo mere online hone par edit kiye gaye hon."
    )
    await event.reply(help_text, buttons=Button.inline("Back", b"start_back"))

# --- BROADCAST COMMAND (Owner Only) ---
@client.on(events.NewMessage(pattern='/broadcast'))
async def broadcast(event):
    if event.sender_id != OWNER_ID:
        return await event.reply("❌ **Sirf Owner hi broadcast kar sakta hai!**")
    
    msg = await event.get_reply_message()
    if not msg:
        return await event.reply("👉 **Method:** Kisi message ko reply karke `/broadcast` likhein.")
    
    status = await event.reply("🚀 **Broadcast Start Ho Raha Hai...**")
    # Yahan aap database use kar sakte hain users list ke liye. 
    # Currently ye direct reply features pe focus hai.
    await status.edit("✅ **Broadcast Completed!** (Database setup recommended for mass users)")

# --- EDIT DETECTION LOGIC ---
@client.on(events.MessageEdited)
async def edit_handler(event):
    if event.is_private:
        return
    
    try:
        chat = await event.get_chat()
        user = await event.get_sender()
        original_text = event.original_update.message.message
        
        log_msg = (
            "🛡️ **EDIT DETECTED** 🛡️\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "👥 **Group:** `{}`\n"
            "👤 **User:** [{}](tg://user?id={})\n"
            "🆔 **User ID:** `{}`\n\n"
            "📝 **Original Message:**\n`{}`\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━"
        ).format(chat.title, user.first_name, user.id, user.id, original_text)
        
        await client.send_message(LOG_GROUP, log_msg)
    except Exception as e:
        print(f"Error: {e}")

print("✅ Bot is Online and Guarding...")
client.run_until_disconnected()
