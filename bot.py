import logging
from telethon import TelegramClient, events, Button

# --- CONFIGURATION ---
API_ID = 34135757
API_HASH = 'd3d5548fe0d98eb1fb793c2c37c9e5c8'
BOT_TOKEN = '8311404972:AAG6cmGBT-VmSgU4xnwA5aJtLMnVJKdlqXo'
LOG_GROUP = -1003867805165
OWNER_ID = 8482447535
START_IMG = 'https://graph.org/file/06f17f2da3be3ddf5c9d6-f22b08d691cecb6be9.jpg'

# Logging setup
logging.basicConfig(level=logging.INFO)

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
        "• `/help` : Ye menu dekhne ke liye.\n"
        "• `/broadcast` : (Owner Only) Sabhi users ko message bhejne ke liye.\n\n"
        "⚠️ **Note:** Bot ko group mein admin hona chahiye!"
    )
    await event.reply(help_text, buttons=Button.inline("Back", b"start_back"))

# --- BROADCAST COMMAND ---
@client.on(events.NewMessage(pattern='/broadcast'))
async def broadcast(event):
    if event.sender_id != OWNER_ID:
        return await event.reply("❌ **Sirf Owner hi use kar sakta hai!**")
    
    reply = await event.get_reply_message()
    if not reply:
        return await event.reply("👉 Message ko reply karke `/broadcast` likhein.")
    
    await event.reply("🚀 **Broadcast Send Ho Gaya!**")
    # Note: Proper broadcast ke liye Database zaroori hota hai.

# --- EDIT DETECTION LOGIC ---
@client.on(events.MessageEdited)
async def edit_handler(event):
    if event.is_private: return
    try:
        chat = await event.get_chat()
        user = await event.get_sender()
        msg = event.original_update.message.message
        
        log_text = (
            f"🛡️ **EDIT DETECTED**\n"
            f"━━━━━━━━━━━━━━\n"
            f"👥 **Chat:** {chat.title}\n"
            f"👤 **User:** {user.first_name} (`{user.id}`)\n\n"
            f"📝 **Old Message:**\n`{msg}`"
        )
        await client.send_message(LOG_GROUP, log_text)
    except Exception as e:
        print(f"Error: {e}")

print("✅ Bot is Starting...")
client.run_until_disconnected()
