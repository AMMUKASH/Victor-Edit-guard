import os
import asyncio
import threading
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from flask import Flask

# ==========================================================
# 🛑 CREDENTIALS & CONFIGURATION (YOU CAN UPDATE OWNER URL)
# ==========================================================
API_ID = 38138069
API_HASH = "2ed313ebcc45cbcf65d1fc736ec71681"
BOT_TOKEN = "8785307171:AAE6ox5IfylJONaBDDM0nr8j0clGizreRwI"
LOG_GROUP = -1003947649552
START_IMG = "https://files.catbox.moe/9eooj2.jpg"

# Buttons Links
SUPPORT_URL = "https://t.me/Genu_Bot_Support"
UPDATE_URL = "https://t.me/Edit_Guardian_Update"
OWNER_URL = "https://t.me/your_owner_username"  # 👈 यहाँ अपना टेलीग्राम यूजरनेम डाल लें

# ==========================================================
# 🌐 FLASK SERVER (Keep-Alive for Render Service)
# ==========================================================
server = Flask(__name__)

@server.route('/')
def home():
    return "𝖤𝖽𝗂𝗍 𝖦𝗎𝖺𝗋𝖽𝗂𝖺𝗇 𝖡𝗈𝗍 𝗂𝗌 𝖠𝗅𝗂𝗏𝖾 𝖺𝗇𝖽 𝖱𝗎𝗇𝗇𝗂𝗇𝗀!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server.run(host="0.0.0.0", port=port)

# ==========================================================
# 🤖 PYROGRAM BOT CLIENT INITIALIZATION
# ==========================================================
app = Client(
    "EditXguardbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

active_chats = set()

# Safe Message Deletion Helper
async def delete_msg(message: Message):
    try:
        await message.delete()
    except Exception:
        pass

# Auto-delete wrapper after a specified delay
async def delete_after_delay(message: Message, delay: int):
    await asyncio.sleep(delay)
    await delete_msg(message)

# Logs Forwarder Helper
async def send_log(client: Client, text: str):
    try:
        await client.send_message(chat_id=LOG_GROUP, text=text)
    except Exception:
        pass

# ==========================================================
# 🎭 STYLISH KEYBOARD BUTTONS PANELS
# ==========================================================
START_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📢 𝖴𝗉𝖽𝖺𝗍𝖾𝗌", url=UPDATE_URL),
        InlineKeyboardButton("💬 𝖲𝗎𝗉𝗉𝗈𝗋𝗍", url=SUPPORT_URL)
    ],
    [
        InlineKeyboardButton("📚 𝖧𝖾𝗅𝗉 & 𝖦𝗎𝗂𝖽𝖾", callback_data="help_guide"),
        InlineKeyboardButton("👑 𝖮𝗐𝗇𝖾𝗋", url=OWNER_URL)
    ],
    [
        InlineKeyboardButton("➕ 𝖠𝖽𝖽 𝖬𝖾 𝖳𝗈 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉", url="https://t.me/EditXguardbot?startgroup=true")
    ]
])

BACK_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔙 𝖡𝖺𝖼𝗄 𝖳𝗈 𝖬𝖾𝗇𝗎", callback_data="back_start")]
])

# ==========================================================
# 📢 PUBLIC & PRIVATE COMMANDS HANDLERS
# ==========================================================

# /start Command (Works Everywhere)
@app.on_message(filters.command("start"))
async def start_cmd(client: Client, message: Message):
    active_chats.add(message.chat.id)
    
    caption = (
        "✨ 𝖶𝖾|𝖼𝗈𝗆𝖾 𝗍𝗈 𝖤𝖽𝗂𝗍 𝖦𝗎𝖺𝗋𝖽𝗂𝖺𝗇 𝖡𝗈𝗍 ✨\n\n"
        "🛡️ 𝖨 𝖺𝗆 𝗁𝖾𝗋𝖾 𝗍𝗈 𝗉𝗋𝗈𝗍𝖾𝖼𝗍 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉s 𝖿𝗋𝗈𝗆 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝖾𝖽𝗂𝗍𝗂𝗇𝗀!\n\n"
        "👤 **𝖴𝗌𝖾𝗋:** {mention}\n\n"
        "» 𝖢|𝗂𝖼𝗄 𝗈𝗇 𝗍𝗁𝖾 **𝖧𝖾𝗅𝗉 & 𝖦𝗎𝗂𝖽𝖾** 𝖻𝗎𝗍𝗍𝗈𝗇 𝖻𝖾|𝗈𝗐 𝗍𝗈 𝗄𝗇𝗈𝗐 𝗁𝗈𝗐 𝗍𝗈 𝗌𝖾𝗍 𝗆𝖾 𝗎𝗉."
    ).format(mention=message.from_user.mention if message.from_user else "𝖴𝗌𝖾𝗋")
    
    if message.chat.type == message.chat.type.PRIVATE:
        await message.reply_photo(photo=START_IMG, caption=caption, reply_markup=START_BUTTONS)
        await send_log(client, f"👤 #𝖲𝖳𝖠𝖱𝖳\n\n𝖴𝗌𝖾𝗋: {message.from_user.mention if message.from_user else '𝖴𝗇𝗄𝗇𝗈𝗐𝗇'}\n𝖨𝖣: `{message.from_user.id if message.from_user else '𝖭/𝖠'}`")
    else:
        await message.reply_text("👋 𝖧𝖾||𝗈! 𝖨 𝖺𝗆 𝖺|𝗂𝗏𝖾 𝖺𝗇𝖽 𝗐𝗈𝗋𝗄𝗂𝗇𝗀. 𝖯|𝖾𝖺𝗌𝖾 𝖯𝖬 𝗆𝖾 𝖿𝗈𝗋 𝗆𝗈𝗋𝖾 𝗂𝗇𝖿𝗈.", reply_markup=START_BUTTONS)

# /help Command (Works Everywhere)
@app.on_message(filters.command("help"))
async def help_cmd(client: Client, message: Message):
    help_text = (
        "📖 **𝖤𝖣𝖨𝖳 𝖦𝖴编𝖱𝖣𝖨𝖠𝖭 𝖦𝖴𝖨𝖣𝖤**\n\n"
        "𝟣. 𝖡𝗈𝗍 𝗄𝗈 𝖺𝗉𝗇𝖾 𝗀𝗋𝗈𝗎𝗉 𝗆𝖾 𝖺𝖽𝖽 𝗄𝖺𝗋𝖾𝗂𝗇.\n"
        "𝟤. 𝖨𝗌𝖾 **𝖣𝖾|𝖾𝗍𝖾 𝖬𝖾𝗌𝗌𝖺𝗀𝖾𝗌** 𝗄𝗂 𝖺𝖽𝗆𝗂𝗇 𝗉𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇 𝖽𝖾𝗂𝗇.\n"
        "𝟥. 𝖡𝖺𝗌! 𝖠𝖻 𝖦𝗋𝗈𝗎𝗉 𝗆𝖾 𝗄𝗈𝗂 𝖻𝗁执行 (𝖠𝖽𝗆𝗂𝗇, 𝖮𝗐𝗇𝖾𝗋, 𝖬𝖾𝗆𝖻𝖾𝗋 𝗒𝖺 𝖡𝗈𝗍) 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝖾𝖽𝗂𝗍 𝗄𝖺𝗋𝖾𝗀𝖺, 𝗍𝗈 𝖻𝗈𝗍 𝗎𝗌𝖾 𝖽𝖾|𝖾𝗍𝖾 𝗄𝖺𝗋 𝖽𝖾𝗀𝖺."
    )
    await message.reply_text(help_text, reply_markup=BACK_BUTTON)

# ==========================================================
# 🎛️ CALLBACK QUERY HANDLER FOR INLINE MENUS
# ==========================================================
@app.on_callback_query()
async def callback_handler(client: Client, query):
    if query.data == "help_guide":
        help_text = (
            "📖 **𝖤𝖣𝖨𝖳 𝖦𝖴编𝖱𝖣𝖨𝖠𝖭 𝖦𝖴𝖨𝖣𝖤**\n\n"
            "𝟣. 𝖡𝗈𝗍 𝗄𝗈 𝖺𝗉𝗇𝖾 𝗀𝗋𝗈𝗎𝗉 𝗆𝖾 𝖺𝖽𝖽 𝗄𝖺𝗋𝖾𝗂𝗇.\n"
            "𝟤. 𝖨𝗌𝖾 **𝖣𝖾|𝖾𝗍𝖾 𝖬𝖾𝗌𝗌𝖺𝗀𝖾𝗌** 𝗄𝗂 𝖺𝖽𝗆𝗂𝗇 𝗉𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇 𝖽𝖾𝗂𝗇.\n"
            "𝟥. 𝖡𝖺𝗌! 𝖠𝖻 𝖦𝗋𝗈𝗎𝗉 𝗆𝖾 𝗄𝗈𝗂 𝖻𝗁执行 (𝖠𝖽𝗆𝗂𝗇, 𝖮𝗐𝗇𝖾𝗋, 𝖬𝖾𝗆𝖻𝖾𝗋 𝗒𝖺 𝖡𝗈𝗍) 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝖾𝖽𝗂𝗍 𝗄𝖺𝗋𝖾𝗀𝖺, 𝗍𝗈 𝖻𝗈𝗍 𝗎𝗌𝖾 𝖽𝖾|𝖾𝗍𝖾 𝗄𝖺𝗋 𝖽𝖾𝗀𝖺."
        )
        try:
            await query.message.edit_caption(caption=help_text, reply_markup=BACK_BUTTON)
        except Exception:
            await query.message.edit_text(text=help_text, reply_markup=BACK_BUTTON)
    
    elif query.data == "back_start":
        caption = (
            "✨ 𝖶𝖾|𝖼𝗈𝗆𝖾 𝗍𝗈 𝖤𝖽𝗂𝗍 𝖦𝗎𝖺𝗋𝖽𝗂𝖺𝗇 𝖡𝗈𝗍 ✨\n\n"
            "🛡️ 𝖨 𝖺𝗆 𝗁𝖾𝗋𝖾 𝗍𝗈 𝗉𝗋𝗈𝗍𝖾𝖼𝗍 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉s 𝖿𝗋𝗈𝗆 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝖾𝖽𝗂𝗍𝗂𝗇𝗀!\n\n"
            "» 𝖢|𝗂𝖼𝗄 𝗈𝗇 𝗍𝗁𝖾 **𝖧𝖾|𝗉 & 𝖦𝗎𝗂𝖽𝖾** 𝖻𝗎𝗍𝗍𝗈𝗇 𝖻𝖾|𝗈𝗐 𝗍𝗈 𝗄𝗇𝗈𝗐 𝗁𝗈𝗐 𝗍𝗈 𝗌𝖾𝗍 𝗆𝖾 𝗎𝗉."
        )
        try:
            await query.message.edit_caption(caption=caption, reply_markup=START_BUTTONS)
        except Exception:
            await query.message.edit_text(text=caption, reply_markup=START_BUTTONS)

# ==========================================================
# 📢 PUBLIC BROADCAST COMMAND (PIN ALL MEMBERS)
# ==========================================================
@app.on_message(filters.command("broadcast"))
async def broadcast_cmd(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("❌ 𝖯|𝖾𝖺𝗌𝖾 𝗋𝖾𝗉|𝗒 𝗍𝗈 𝖺 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗍𝗈 𝖻𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍!")
        return
        
    msg = await message.reply_text("⚡ 𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍𝗂𝗇𝗀 𝗂𝗇 𝗉𝗋𝗈𝗀𝗋𝖾𝗌𝗌...")
    success = 0
    
    for chat_id in list(active_chats):
        try:
            copied_msg = await message.reply_to_message.copy(chat_id=chat_id)
            try:
                await copied_msg.pin(disable_notification=False)
            except:
                pass
            success += 1
        except Exception:
            pass
            
    await msg.edit_text(f"📢 𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖢𝗈𝗆𝗉|𝖾𝗍𝖾𝖽!\n\n✅ 𝖲𝖾𝗇𝗍 𝖺𝗇𝖽 𝖯执行𝗇𝗇𝖾𝖽 𝗂𝗇 {success} 𝖼𝗁𝖺𝗍𝗌.")

# ==========================================================
# 🔔 SERVICE LOGS SYSTEM (AddMe, Start, Leave)
# ==========================================================
@app.on_message(filters.new_chat_members)
async def service_add_log(client: Client, message: Message):
    active_chats.add(message.chat.id)
    for member in message.new_chat_members:
        if member.id == (await client.get_me()).id:
            log_text = (
                f"📥 #𝖠𝖣𝖣𝖬𝖤\n\n"
                f"𝖦𝗋𝗈𝗎𝗉 𝖭𝖺𝗆𝖾: {message.chat.title}\n"
                f"𝖦𝗋𝗈𝗎𝗉 𝖨𝖖: `{message.chat.id}`\n"
                f"𝖠𝖽𝖽𝖾𝖽 𝖡𝗒: {message.from_user.mention if message.from_user else '𝖴𝗇执行𝗇𝗈𝗐𝗇'}"
            )
            await send_log(client, log_text)

@app.on_message(filters.left_chat_member)
async def service_leave_log(client: Client, message: Message):
    if message.left_chat_member.id == (await client.get_me()).id:
        if message.chat.id in active_chats:
            active_chats.remove(message.chat.id)
        log_text = (
            f"📤 #𝖫𝖤𝖠𝖵𝖤\n\n"
            f"𝖦𝗋𝗈𝗎𝗉 𝖭𝖺𝗆𝖾: {message.chat.title}\n"
            f"𝖦𝗋𝗈𝗎𝗉 𝖨𝖖: `{message.chat.id}`"
        )
        await send_log(client, log_text)

# ==========================================================
# 🔥 EDIT GUARDIAN CORE FUNCTION (BEST PRE-VIP DESIGN)
# ==========================================================
@app.on_edited_message(filters.group)
async def handle_edited_message(client: Client, message: Message):
    try:
        active_chats.add(message.chat.id)
        
        # User details processing
        user = message.from_user
        mention = user.mention if user else "𝖴𝗇执行𝗇𝗈𝗐𝗇 𝖴saf"
        username = f"@{user.username}" if user and user.username else "𝖭𝗈 𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾"
        
        # Super Stylish Aesthetic VIP Layout (Ref: 1000005352.png concept upgraded)
        text = (
            f"╔══════════════════════╗\n"
            f"   🚨 **𝖤𝖣𝖨𝖳  𝖣𝖤𝖳𝖤𝖢𝖳𝖤𝖣  𝖠𝖫𝖤𝖱𝖳** 🚨\n"
            f"╚══════════════════════╝\n\n"
            f"🚫 **𝖧𝖾𝗒 {mention}, 𝖤𝖽𝗂𝗍𝗂𝗇𝗀 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝗂𝗌 𝗌𝗍𝗋𝗂𝖼𝗍|𝗒**\n"
            f"**𝗉𝗋𝗈𝗁𝗂𝖻𝗂𝗍𝖾𝖽 𝗁𝖾𝗋𝖾 𝖽𝗎𝖾 𝗍𝗈 𝖼𝗈𝗉𝗒𝗋𝗂𝗀𝗁𝗍 & 𝗌𝖺𝖿𝖾𝗍𝗒!**\n\n"
            f"📝 **𝖴𝗌𝖾𝗋 𝖨𝗇𝖿𝗈𝗋𝗆𝖺𝗍𝗂𝗈𝗇:**\n"
            f"  » 👤 **𝖭𝖺𝗆𝖾:** {mention}\n"
            f"  » 🌐 **𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾:** {username}\n"
            f"  » 🆔 **𝖴𝗌𝖾𝗋 𝖨𝖣:** `{user.id if user else '𝖭/𝖠'}`\n\n"
            f"🗑️ `𝖸𝗈𝗎𝗋 𝗈𝗋执行𝗀𝗂𝗇𝖺| 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗁𝖺𝗌 𝖻𝖾𝖾𝗇 𝖽𝖾|𝖾𝗍𝖾𝖽.`\n\n"
            f"⏳ __𝖳𝗁𝗂𝗌 𝗐𝖺𝗋𝗇𝗂𝗇𝗀 𝗐𝗂𝗅𝗅 𝖺𝗎𝗍𝗈-𝖽𝖾|𝖾𝗍𝖾 𝗂𝗇 𝟨𝟢𝗌.__\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
        
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📢 Updates", url=UPDATE_URL),
                InlineKeyboardButton("💬 Support", url=SUPPORT_URL)
            ],
            [
                InlineKeyboardButton("👑 Contact Owner", url=OWNER_URL)
            ]
        ])
        
        # 1. Delete original edited message immediately (For Everyone: Owner/Admin/Bots/Users)
        await delete_msg(message)
        
        # 2. Send premium warning layout alert to group
        warning_msg = await client.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=buttons
        )
        
        # 3. Schedule automatic self-destruction of the alert after 60 seconds
        asyncio.create_task(delete_after_delay(warning_msg, 60))
        
    except Exception as e:
        print(f"VIP Edit Handler Error: {e}")

# ==========================================================
# RUN APPLICATION WITH THREADED FLASK
# ==========================================================
if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    print("✨ @EditXguardbot is starting up successfully...")
    app.run()
