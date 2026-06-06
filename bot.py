import os
import re
import asyncio
import datetime
from aiohttp import web
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from pymongo import MongoClient
from config import API_ID, API_HASH, BOT_TOKEN, LOG_GROUP, PORT, START_IMG, BOT_USERNAME, UPDATE_CH, SUPPORT_CH, OWNER_ID, OWNER_USERNAME

# MongoDB Connection Configuration with Your Exact Fallback
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://misssqn_db_user:Nova01@cluster0.6xxsrwq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Database Setup
mongo_client = MongoClient(MONGO_URL)
db = mongo_client["NovaDB"]
users_col = db["registered_users"]  
groups_col = db["registered_groups"]  

# Initialize Pyrogram Client
bot = Client("BioLinkerBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# URL matching regex
URL_PATTERN = re.compile(r'(https?://[^\s]+|t\.me/[^\s]+|@\w+\.\w+|www\.[^\s]+)')

# Stylish UI Strings
START_TXT = """
✨ ⚡ **ʙɪᴏ ʟɪɴᴋ ʀᴇᴍᴏᴠᴇʀ ʙᴏᴛ** ⚡ ✨
━━━━━━━━━━━━━━━━━━━━━━━━━━━

👋 **ʜᴇʟʟᴏ** {mention} !

ᴍᴀɪɴ ᴇᴋ ⚡ **ᴀᴅᴠᴀɴᴄᴇᴅ sᴇᴄᴜʀɪᴛʏ ʙᴏᴛ** ʜᴏᴏɴ ᴊᴏ ᴀᴀᴘᴋᴇ ɢʀᴏᴜᴘs ᴋᴏ sᴘᴀᴍᴍᴇʀs ᴀᴜʀ sᴇʟғ-ᴘʀᴏᴍᴏᴛᴇʀs sᴇ sᴀғᴇ ʀᴀᴋʜᴛᴀ ʜᴀɪ.

┌───────────────────────┐
│ 🛡️ **<b>ᴄᴏʀᴇ ғᴇᴀᴛᴜʀᴇs :</b>**
├───────────────────────┤
│ 👤 **ʙɪᴏ sᴄᴀɴɴᴇʀ:** Automated Bio Scan
│ 🗑️ **ᴍᴇssᴀɢᴇ ᴅᴇʟᴇᴛᴇ:** Instant Clean Up
└───────────────────────┘

🚀 **ʜᴏᴡ ᴛᴏ ᴜsᴇ?**
🟪 ᴍᴜᴊʜᴇ ᴀᴘɴᴇ ɢʀᴏᴜᴘ ᴍᴇɪɴ **ᴀᴅᴍɪɴ** ʙᴀɴᴀʏᴇɪɴ.
🟪 `Delete Messages` & `Ban Users` ᴘᴇʀᴍɪssɪᴏɴs ᴀʟʟᴏᴡ ᴋᴀʀᴇɪɴ.

━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️ **sᴛᴀᴛᴜs:** `🤖 sʏsᴛᴇᴍ ᴏɴʟɪɴᴇ`
"""

HELP_TXT = """
⚙️ **ʜᴇʟᴘ & ɢᴜɪᴅᴇ ᴍᴇɴᴜ** ⚙️
━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 **ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs:**
🔹 `/start` - Check bot status (Private/Groups)
🔹 `/help` - Open this assistance window
🔹 `/broadcast` - Send alert to database (Owner Only)

⚙️ **ʜᴏᴡ ɪᴛ ᴡᴏʀᴋs:**
⚠️ **ᴠɪᴏʟᴀᴛɪᴏɴ:** Agar kisi user ki Bio me Link mila, toh bot uske message ko **ɪɴsᴛᴀɴᴛ ᴅᴇʟᴇᴛᴇ** kar dega.

💡 *ɴᴏᴛᴇ: Group Admins aur Creator par security filter run nahi hota.*
"""

MAIN_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("🤖 ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ 🤖", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
    [InlineKeyboardButton("👑 ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}"),
     InlineKeyboardButton("⚙️ ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="help_menu")],
    [InlineKeyboardButton("🔕 ᴜᴘᴅᴀᴛᴇ", url=f"https://t.me/{UPDATE_CH}"),
     InlineKeyboardButton("💌 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CH}")]
])

BACK_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="back_home")]
])

async def is_user_admin(chat_id, user_id):
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except:
        return False

# Start Command Handler
@bot.on_message(filters.command("start"))
async def start_cmd(client, message: Message):
    user = message.from_user
    if not user: return
    
    if message.chat.type == "private":
        if not users_col.find_one({"user_id": user.id}):
            users_col.insert_one({"user_id": user.id, "date": datetime.datetime.now()})
            log_msg = f"👤 **#New_User_Start**\n\n**User:** {user.mention}\n**ID:** `{user.id}`"
            try: await bot.send_message(chat_id=LOG_GROUP, text=log_msg)
            except: pass

    try:
        await message.reply_photo(
            photo=START_IMG,
            caption=START_TXT.format(mention=user.mention),
            reply_markup=MAIN_BUTTONS
        )
    except Exception:
        await message.reply_text(
            text=START_TXT.format(mention=user.mention),
            reply_markup=MAIN_BUTTONS
        )

# Help Command Handler
@bot.on_message(filters.command("help"))
async def help_cmd(client, message: Message):
    await message.reply_text(text=HELP_TXT, reply_markup=BACK_BUTTON)

# Callback Query Handler
@bot.on_callback_query()
async def callback_handler(client, query):
    user = query.from_user
    if query.data == "help_menu":
        try: await query.message.edit_caption(caption=HELP_TXT, reply_markup=BACK_BUTTON)
        except: await query.message.edit_text(text=HELP_TXT, reply_markup=BACK_BUTTON)
    elif query.data == "back_home":
        try: await query.message.edit_caption(caption=START_TXT.format(mention=user.mention), reply_markup=MAIN_BUTTONS)
        except: await query.message.reply_text(text=START_TXT.format(mention=user.mention), reply_markup=MAIN_BUTTONS)

# Tracking Bot addition to groups
@bot.on_message(filters.new_chat_members)
async def bot_added_to_chat(client, message: Message):
    for member in message.new_chat_members:
        if member.id == (await bot.get_me()).id:
            chat = message.chat
            if not groups_col.find_one({"chat_id": chat.id}):
                groups_col.insert_one({"chat_id": chat.id, "date": datetime.datetime.now()})
            log_msg = f"📥 **#Added_To_New_Group**\n\n**Group:** {chat.title}\n**ID:** `{chat.id}`"
            try: await bot.send_message(chat_id=LOG_GROUP, text=log_msg)
            except: pass

# Core Anti-Bio Link Logic (SILENT MESSAGE DELETE + ALERT BUTTONS)
@bot.on_message(filters.group & ~filters.service)
async def check_bio_and_delete(client, message: Message):
    if not message.from_user: return
    user_id = message.from_user.id
    chat_id = message.chat.id
    chat_title = message.chat.title

    if await is_user_admin(chat_id, user_id): return

    print(f"🔍 [SCANNER] Processing message from user {user_id} in chat {chat_id}")

    try:
        member_info = await client.get_chat_member(chat_id, user_id)
        user_info = member_info.user
        
        bio = getattr(user_info, "bio", None)
        if bio is None:
            full_user = await client.get_users(user_id)
            bio = full_user.bio

        print(f"📝 [SCANNER] User Bio text resolved: '{bio}'")

        if bio and URL_PATTERN.search(bio):
            print(f"⚠️ [SCANNER] Match found! Bio contains spam link. Deleting message...")
            await message.delete()
            
            # Action Buttons: Add Me + Update + Support
            action_buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("🤖 ᴀᴅᴅ ᴍᴇ 🤖", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
                [InlineKeyboardButton("🔕 ᴜᴘᴅᴀᴛᴇ", url=f"https://t.me/{UPDATE_CH}"),
                 InlineKeyboardButton("💌 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CH}")]
            ])

            await message.reply_text(
                text=f"⚠️ ⚡ **ᴍᴇssᴀɢᴇ ᴅᴇʟᴇᴛᴇᴅ** ⚡ ⚠️\n\n👤 **ᴜsᴇʀ:** {message.from_user.mention}\n🆔 **ᴜsᴇʀ ɪᴅ:** `{user_id}`\n👥 **ɢʀᴏᴜᴘ:** `{chat_title}`\n📝 **ʀᴇᴀsᴏɴ:** Link detected in user Bio. Message removed silently.",
                reply_markup=action_buttons
            )
    except Exception as e:
        print(f"❌ [SCANNER ERROR] Failed to evaluate bio logic: {e}")

# Async Broadcast Engine 
async def send_broadcast_msg(client, chat_id, reply_msg, pin):
    try:
        m = await reply_msg.copy(chat_id)
        if pin: await m.pin(both_sides=True)
        return "success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_broadcast_msg(client, chat_id, reply_msg, pin)
    except Exception: return "failed"

# Advanced Broadcast & Gcast Handler
@bot.on_message(filters.command(["broadcast", "gcast"]) & (filters.user(OWNER_USERNAME) | filters.user(OWNER_ID)))
async def broadcast_handler(client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("❌ **Reply to a message with:**\n`/broadcast all` or `users` or `groups` (add `-pin` if you want to pin it)")
        return
        
    cmd_args = message.text.split()
    b_type = cmd_args[1].lower() if len(cmd_args) > 1 else "all"
    pin = "-pin" in message.text.lower()
    
    status_msg = await message.reply_text("⚡ **ʙʀᴏᴀᴅᴄᴀsᴛ sᴛᴀʀᴛɪɴɢ...**")
    targets = []
    
    if b_type in ["all", "users"]: 
        targets.extend([u["user_id"] for u in users_col.find({})])
    if b_type in ["all", "groups"]: 
        targets.extend([g["chat_id"] for g in groups_col.find({})])
        
    targets = list(set(targets))
    
    if not targets:
        await status_msg.edit_text("❌ Database me koi users ya groups nahi mile!")
        return

    success = 0
    failed = 0
    
    for t_id in targets:
        res = await send_broadcast_msg(client, t_id, message.reply_to_message, pin)
        if res == "success": success += 1
        else: failed += 1
        await asyncio.sleep(0.3)
        
    await status_msg.edit_text(f"📢 **ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ**\n\n✅ **sᴜᴄᴄᴇss:** `{success}`\n❌ **ғᴀɪʟᴇᴅ:** `{failed}`")

# HTTP Server Route to feed Render's port binder
async def web_handle(request):
    return web.Response(text="Bot Engine is fully functional and live 24/7! 🚀")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ⚙️ COMPATIBILITY RUNNER FOR WEB PORT BINDING & ASYNC CLIENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
async def main():
    print("⚡ Starting Pyrogram Client Engine...")
    await bot.start()
    print("🤖 Bot is successfully online!")
    
    app = web.Application()
    app.router.add_get('/', web_handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    print(f"📡 Web Server tightly bound and active on port {PORT}")
    
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
