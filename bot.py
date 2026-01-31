import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- CONFIGURATION ---
API_ID = 34135757
API_HASH = "d3d5548fe0d98eb1fb793c2c37c9e5c8"
BOT_TOKEN = "8311404972:AAG6cmGBT-VmSgU4xnwA5aJtLMnVJKdlqXo"

# IDs & Links
OWNER_ID = 8482447535
LOG_GROUP = -1003867805165
SUPPORT_GRP = "https://t.me/+PKYLDIEYiTljMzMx"
UPDATE_CHN = "https://t.me/radhesupport"
OWNER_LINK = "https://t.me/XenoEmpir"
START_IMG = "https://graph.org/file/3e0a6b443746a0e015d72-c32a268e5c7ec2feb4.jpg"

app = Client("GuardBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Forbidden Keywords
BANNED_TAGS = ["porn", "sex", "kiss", "hot", "sexy", "nsfw", "18+", "pussy", "dick", "xxx"]

# --- BUTTONS ---
START_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📢 Updates", url=UPDATE_CHN),
        InlineKeyboardButton("🎧 Support", url=SUPPORT_GRP)
    ],
    [
        InlineKeyboardButton("👤 Owner", url=OWNER_LINK),
        InlineKeyboardButton("🛠 Help & Guide", callback_data="help_data")
    ]
])

# --- FUNCTIONS ---

# Start Message with Photo
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(bot, message):
    await message.reply_photo(
        photo=START_IMG,
        caption=(f"✨ **Hello {message.from_user.mention}!**\n\n"
                 "I am your advanced **NSFW Guard Bot**.\n\n"
                 "🛡 I protect groups from inappropriate content, stickers, and text.\n"
                 "👤 **Owner:** [Xeno](https://t.me/XenoEmpir)\n\n"
                 "Add me to your group and make me admin to start!"),
        reply_markup=START_BUTTONS
    )

# Welcome New Members
@app.on_message(filters.new_chat_members)
async def welcome_member(bot, message):
    for member in message.new_chat_members:
        await message.reply_text(
            f"👋 Hello {member.mention}, welcome to **{message.chat.title}**!\n"
            "Please follow the rules and stay safe."
        )

# NSFW Filter (Media, Stickers, GIFs)
@app.on_message(filters.group & (filters.photo | filters.video | filters.animation | filters.sticker))
async def nsfw_media_filter(bot, message):
    check_text = ""
    if message.animation and message.animation.file_name:
        check_text = message.animation.file_name.lower()
    elif message.sticker and message.sticker.set_name:
        check_text = message.sticker.set_name.lower()
    
    if any(word in check_text for word in BANNED_TAGS):
        try:
            await message.delete()
            # Send Log to Log Group
            log_text = (f"🚨 **NSFW Media Detected**\n\n"
                        f"👤 **User:** {message.from_user.mention} (`{message.from_user.id}`)\n"
                        f"👥 **Group:** {message.chat.title}\n"
                        f"🚫 **Action:** Message Deleted")
            await bot.send_message(LOG_GROUP, log_text)
        except Exception:
            pass

# NSFW Text Filter
@app.on_message(filters.group & filters.text & ~filters.command(["start", "help", "broadcast"]))
async def nsfw_text_filter(bot, message):
    if any(word in message.text.lower() for word in BANNED_TAGS):
        try:
            await message.delete()
            # Log to Log Group
            log_text = (f"🚨 **NSFW Text Detected**\n\n"
                        f"👤 **User:** {message.from_user.mention}\n"
                        f"💬 **Text:** `{message.text[:100]}`\n"
                        f"🚫 **Action:** Message Deleted")
            await bot.send_message(LOG_GROUP, log_text)
        except Exception:
            pass

# Help Command
@app.on_message(filters.command("help"))
async def help_command(bot, message):
    guide = (
        "**📚 GuardBot Help Guide**\n\n"
        "1️⃣ Add me to your group.\n"
        "2️⃣ Promote me as Admin.\n"
        "3️⃣ Give 'Delete Messages' permission.\n\n"
        "I will automatically scan and remove NSFW stickers, GIFs, and text messages."
    )
    await message.reply_text(guide)

# Simple Broadcast (Owner Only)
@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(bot, message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Please reply to a message to broadcast.")
    
    await message.reply_text("🔄 **Broadcast feature initiated...**\n(Note: Connect a database for global group messaging.)")

# --- RUN BOT ---
if __name__ == "__main__":
    print("-----------------------")
    print("GuardBot is now Online!")
    print("-----------------------")
    app.run()
