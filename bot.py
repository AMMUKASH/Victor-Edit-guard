# ==========================================================
# 🛑 CRITICAL PYTHON 3.14+ FIX: INITIALIZE LOOP BEFORE IMPORTS
# ==========================================================
import asyncio
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# अब सारे इम्पोर्ट्स सेफली काम करेंगे
import os
import threading
from collections import deque
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.methods.utilities.idle import idle
from flask import Flask
from motor.motor_asyncio import AsyncIOMotorClient

# raw updates हैंडल करने के लिए इम्पोर्ट्स (रिएक्शन ब्लॉक करने के लिए)
from pyrogram.raw.types import UpdateEditMessage, UpdateEditChannelMessage

# ==========================================================
# 🛑 CREDENTIALS & CONFIGURATION
# ==========================================================
API_ID = 38138069
API_HASH = "2ed313ebcc45cbcf65d1fc736ec71681"
BOT_TOKEN = "8785307171:AAE6ox5IfylJONaBDDM0nr8j0clGizreRwI"
LOG_GROUP = -1003947649552
START_IMG = "https://files.catbox.moe/9eooj2.jpg"

# 🌐 MONGODB CONNECTION
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://misssqn_db_user:Nova01@cluster0.6xxsrwq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Buttons Links
SUPPORT_URL = "https://t.me/Genu_Bot_Support"
UPDATE_URL = "https://t.me/Edit_Guardian_Update"
OWNER_URL = "https://t.me/CoderNova"

# ==========================================================
# 🧠 MEMORY CACHE SYSTEM (50,000 MESSAGES CAPACITY)
# ==========================================================
CACHE_MAX_SIZE = 50000
MESSAGE_TEXT_CACHE = {}
CACHE_KEYS_TRACKER = deque()

def add_to_cache(cache_key, text):
    if cache_key not in MESSAGE_TEXT_CACHE:
        CACHE_KEYS_TRACKER.append(cache_key)
    
    MESSAGE_TEXT_CACHE[cache_key] = text
    
    if len(CACHE_KEYS_TRACKER) > CACHE_MAX_SIZE:
        oldest_key = CACHE_KEYS_TRACKER.popleft()
        MESSAGE_TEXT_CACHE.pop(oldest_key, None)

# ==========================================================
# 🗄️ DATABASE SETTINGS (MONGODB)
# ==========================================================
db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client["EditXguardbot_DB"]
chats_col = db["active_chats"]

async def add_chat(chat_id):
    try:
        await chats_col.update_one({"chat_id": chat_id}, {"$set": {"chat_id": chat_id}}, upsert=True)
    except Exception as e:
        print(f"DB Error (Add): {e}")

async def remove_chat(chat_id):
    try:
        await chats_col.delete_one({"chat_id": chat_id})
    except Exception as e:
        print(f"DB Error (Remove): {e}")

async def get_all_chats():
    try:
        cursor = chats_col.find({})
        chats = await cursor.to_list(length=10000)
        return [doc["chat_id"] for doc in chats]
    except Exception as e:
        print(f"DB Error (Get All): {e}")
        return []

# ==========================================================
# 🌐 FLASK SERVER (Keep-Alive for Render Service)
# ==========================================================
server = Flask(__name__)

@server.route('/')
def home():
    return "𝖤𝖽𝗂𝗍 𝖦𝗎𝖺𝗋𝖽𝗂𝖺𝗇 𝖡𝗈𝗍 𝗂𝗌 𝖠|𝗂𝗏𝖾 𝖺𝗇𝖽 𝖱𝗎𝗇𝗇𝗂่น𝗀!"

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
        InlineKeyboardButton("📢 𝖴𝗉𝖽𝖺𝖾𝗌", url=UPDATE_URL),
        InlineKeyboardButton("💬 𝖲𝗎𝗉𝗉𝗈𝗋𝗍", url=SUPPORT_URL)
    ],
    [
        InlineKeyboardButton("📚 𝖧𝖾|𝗉 & 𝖦𝗎𝗂𝖽𝖾", callback_data="help_guide"),
        InlineKeyboardButton("👑 𝖮𝗐𝗇𝖾𝗋", url=OWNER_URL)
    ],
    [
        InlineKeyboardButton("➕ 𝖠𝖽𝖽 𝖬𝖾 𝖳𝗈 𝖸𝗈𝗎𝗋 𝖦𝗋ᅩ𝗎𝗉", url="https://t.me/EditXguardbot?startgroup=true")
    ]
])

BACK_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔙 𝖡𝖺𝖼𝗄 𝖳𝗈 𝖬𝖾𝗇𝑢", callback_data="back_start")]
])

# ==========================================================
# 📢 PUBLIC & PRIVATE COMMANDS HANDLERS
# ==========================================================

# आने वाले हर नए मैसेज का टेक्स्ट स्टोर करने के लिए
@app.on_message(filters.group & (filters.text | filters.caption) & ~filters.bot, group=-1)
async def cache_incoming_messages(client: Client, message: Message):
    current_text = message.text or message.caption
    if current_text:
        cache_key = f"{message.chat.id}_{message.id}"
        add_to_cache(cache_key, current_text)

@app.on_message(filters.command("start"))
async def start_cmd(client: Client, message: Message):
    await add_chat(message.chat.id)
    caption = (
        "✨ 𝖶𝖾|𝖼𝗈𝗆𝖾 𝗍𝗈 𝖤𝖽𝗂𝗍 𝖦𝗎𝖺𝗋𝖽𝗂𝖺𝗇 𝖡𝗈𝗍 ✨\n\n"
        "🛡️ 𝖨 𝖺𝗆 𝗁𝖾𝗋𝖾 𝗍𝗈 𗗗𝗋𝗈𝗍𝖾𝖼𝗍 𝗒𝗈𝗎𝗋 𗗗𝗋𝗈𝗎𝗉𝗌 𝖿𝗋𝗈𝗆 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝖾𝖽𝗂𝗍𝗂𝗇𝗀!\n\n"
        "👤 **𝖴𝗌𝖾𝗋:** {mention}\n\n"
        "» 𝖢|𝗂𝖼𝗄 𝗈𝗇 𝗍𝗁𝖾 **𝖧𝖾|𝗉 & 𝖦𝗎𝗂𝖽𝖾** 𝖻𝗎𝗍𝗍𝗈𝗇 𝖻𝖾|𝗈𝗐 𝗍𝗈 <b>𝗄𝗇𝗈𝗐</b> <b>𝗁𝗈𝗐</b> 𝗍𝗈 𝗌𝖾𝗍 𝗆𝖾 𝗎𝗉."
    ).format(mention=message.from_user.mention if message.from_user else "𝖴𝗌𝖾𝗋")
    
    if message.chat.type == message.chat.type.PRIVATE:
        await message.reply_photo(photo=START_IMG, caption=caption, reply_markup=START_BUTTONS)
        await send_log(client, f"👤 #𝖲𝖳𝖠𝖱𝖳\n\n𝖴𝗌𝖾𝗋: {message.from_user.mention if message.from_user else '𝖴𝗇𝗄𝗇𝗈𝗐𝗇'}\n𝖨𝖣: `{message.from_user.id if message.from_user else '𝖭/𝖠'}`")
    else:
        await message.reply_text("👋 𝖧𝖾||𝗈! 𝖨 𝖺𝗆 𝖺|𝗂𝗏𝖾 𝖺𝗇𝖽 𝗈𝗋𝗄𝗂𝗇𝗀. 𝖯|𝖾𝖺𝗌𝖾 𝖯𝖬 𝗆𝖾 𝖿𝗈𝗋 𝗆𝗈𝗋𝖾 𝗂𝗇𝖿𝗈.", reply_markup=START_BUTTONS)

@app.on_message(filters.command("help"))
async def help_cmd(client: Client, message: Message):
    help_text = (
        "📖 **𝖤𝖣𝖨𝖳 𝖦𝖴𝖠𝖱𝖣𝖨index𝖠𝖭 𝖦𝖴𝖨𝖣𝖤**\n\n"
        "𝟣. 𝖡𝗈𝗍 𝗄𝗈 𝖺𝗉𝗇𝖾 𗗗𝗋𝗈𝗎𝗉 𝗆𝖾 𝖺𝖽𝖽 <b>𝗄𝖺𝗋𝖾𝗂𝗇</b>.\n"
        "𝟤. 𝖨𝗌𝖾 **𝖣𝖾|𝖾𝗍𝖾 𝖬𝖾𝗌𝗌𝖺𝗀𝖾𝗌** 𝗄𝗂 𝖺𝖽𝗆𝗂𝗇 𗗗𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈ၼ် 𝖽𝖾𝗂𝗇.\n"
        "𝟥. 𝖡𝖺𝗌! <b>𝖠𝖻</b> 𗗗𝗋𝗈𝗎𝗉 <b>𝗆𝖾</b> 𝗄𝗈𝗂 𝖻𝗁𝗂 (𝖠𝖽𝗆𝗂𝗇, 𝖮𗗗𝗇𝖾𝗋, 𝖬𝖾𝗆𝖻𝖾𝗋 𗗗𝖺 𝖡𝗈𝗍) 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝖾𝖽𝗂𝗍 𝗄𝖺𝗋𝖾𝗀𝖺, 𝗍𝗈 𝖻<b>𝗈𝗍</b> 𝗎𝗌𝖾 𝖽𝖾|𝖾𝗍𝖾 𝗄𝖺𝗋 𝖽𝖾𝗀𝖺."
    )
    await message.reply_text(help_text, reply_markup=BACK_BUTTON)

@app.on_callback_query()
async def callback_handler(client: Client, query):
    if query.data == "help_guide":
        help_text = (
            "📖 **𝖤𝖣𝖨𝖳 𝖦𝖴𝖠𝖱𝖣𝖨𝖠𝖭 𝖦𝖴𝖨𝖣𝖤**\n\n"
            "𝟣. 𝖡𝗈𝗍 𝗄𝗈 𝖺𝗉𝗇𝖾 𗗗𝗋𝗈𝗎𝗉 𝗆𝖾 𝖺𝖽𝖽 𝗄𝖺𝗋𝖾𝗂𝗇.\n"
            "𝟤. 𝖨𝗌𝖾 **𝖣𝖾|𝖾𝗍𝖾 𝖬𝖾𝗌𝗌𝖺𝗀𝖾𝗌** 𝗄𝗂 𝖺𝖽𝗆𝗂𝗇 𗗗𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇 <b>𝖽𝖾𝗂𝗇</b>.\n"
            "𗟵. 𝖡𝖺𝗌! 𝖠𝖻 𗗗𝗋𝗈𝗎𝗉 𝗆𝖾 𝗄𝗈𝗂 𝖻<b>𝗁𝗂</b> (𝖠𝖽𝗆𝗂𝗇, 𝖮𗗗𝗇𝖾𝗋, 𝖬𝖾𝗆𝖻𝖾𝗋 𗗗𝖺 𝖡𝗈𝗍) 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝖾𝖽𝗂𝗍 𝗄𝖺𝗋𝖾𝗀𝖺, 𝗍𝗈 𝖻𝗈𝗍 𝗎𝗌𝖾 𝖽𝖾|𝖾𝗍𝖾 <b>𝗄𝖺𝗋</b> 𝖽𝖾𝗀𝖺."
        )
        try:
            await query.message.edit_caption(caption=help_text, reply_markup=BACK_BUTTON)
        except Exception:
            await query.message.edit_text(text=help_text, reply_markup=BACK_BUTTON)
    elif query.data == "back_start":
        caption = (
            "✨ 𝖶𝖾|𝖼𝗈𝗆𝖾 𝗍𝗈 𝖤𝖽𝗂𝗍 𝖦𝗎𝖺𝗋𝖽𝗂𝖺𝗇 𝖡𝗈𝗍 ✨\n\n"
            "🛡️ 𝖨 𝖺𝗆 𝗁𝖾𝗋𝖾 𝗍𝗈 𗗗𝗋𝗈𝗍𝖾𝖼𝗍 𝗒<b>𝗈𝗎𝗋</b> 𗗗𝗋𝗈𝗎𝗉𝗌 𝖿𝗋𝗈𝗆 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝖾𝖽𝗂𝗍𝗂𝗇𝗀!\n\n"
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
        
    msg = await message.reply_text("⚡ 𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍𝗂𝗇𝗀 𝗂𝗇 𗗗𝗋𝗈𝗀𝗋𝖾𝗌..." )
    success = 0
    all_chats = await get_all_chats()
    
    for chat_id in all_chats:
        try:
            copied_msg = await message.reply_to_message.copy(chat_id=chat_id)
            try:
                await copied_msg.pin(disable_notification=False)
            except:
                pass
            success += 1
        except Exception:
            await remove_chat(chat_id)
            
    await msg.edit_text(f"📢 𝖡𝗋ོ་𝖺𝖽𝖼𝖺𝗌𝗍 𝖢𝗈𝗆𝗉|𝖾𝗍𝖾𝖽!\n\n✅ 𝖲𝖾𝗇𝗍 𝖺𝗇𝖽 𝖯𝗂𝗇𝗇𝖾𝖽 𝗂𝗇 {success} 𝖼𝗁𝖺𝗍𝗌.")

# ==========================================================
# 🔔 SERVICE LOGS SYSTEM
# ==========================================================
@app.on_message(filters.new_chat_members)
async def service_add_log(client: Client, message: Message):
    for member in message.new_chat_members:
        if member.id == (await client.get_me()).id:
            await add_chat(message.chat.id)
            log_text = (
                f"📥 #𝖠𝖣𝖣𝖬𝖤\n\n"
                f"𝖦𝗋𝗈𝗎𝗉 𝖭𝖺𝗆𝖾: {message.chat.title}\n"
                f"𝖦𝗋𝗈𝗎𝗉 𝖨𝖣: `{message.chat.id}`\n"
                f"𝖠𝖽𝖽𝖾𝖽 𝖡𝗒: {message.from_user.mention if message.from_user else '𝖴𝗇𝗄𝗇𝗈𝗐𝗇'}"
            )
            await send_log(client, log_text)

@app.on_message(filters.left_chat_member)
async def service_leave_log(client: Client, message: Message):
    if message.left_chat_member.id == (await client.get_me()).id:
        await remove_chat(message.chat.id)
        log_text = (
            f"📤 #𝖫𝖤𝖠𝖵𝖤\n\n"
            f"𝖦𝗋𝗈𝗎𝗉 𝖭𝖺𝗆𝖾: {message.chat.title}\n"
            f"𝖦𝗋𝗈𝗎𝗉 𝖨𝖣: `{message.chat.id}`"
        )
        await send_log(client, log_text)

# ==========================================================
# 🔥 EDIT GUARDIAN CORE FUNCTION (100% REACTION PROOF VIA RAW FILTERS)
# ==========================================================
# कस्टम फ़िल्टर: यह केवल तभी आगे बढ़ेगा जब टेलीग्राम से आने वाला अपडेट 'सच्चा एडिट' (UpdateEditMessage) हो।
# अगर केवल रिएक्शन आएगा, तो टेलीग्राम बैकएंड में अलग अपडेट भेजता है, जिसे यह फ़िल्टर यहीं रोक देगा।
async def raw_edit_filter(_, client: Client, message: Message):
    # अगर बोट का अपना मैसेज है या कोई और बोट है, तो तुरंत छोड़ दो
    if message.from_user and message.from_user.is_bot:
        return False
        
    # Pyrogram के इंटरनल रॉ अपडेट्स चेक करें
    raw_updates = getattr(client, "_raw_updates", [])
    if raw_updates:
        for update in raw_updates:
            # केवल तभी True रिटर्न करें जब अपडेट असली टेक्स्ट/मीडिया एडिट का हो
            if isinstance(update, (UpdateEditMessage, UpdateEditChannelMessage)):
                return True
        return False
    
    # सेफ साइड के लिए: अगर रॉ अपडेट्स लिस्ट खाली है, तो सामान्य चेकिंग पर वापस जाएँ
    return True

only_true_edits = filters.create(raw_edit_filter)

@app.on_edited_message(filters.group & ~filters.bot & only_true_edits)
async def handle_edited_message(client: Client, message: Message):
    new_text = message.text or message.caption
    if not new_text:
        return

    cache_key = f"{message.chat.id}_{message.id}"
    
    # चेक करें कि क्या यह मैसेज मेमोरी कैश में है
    if cache_key in MESSAGE_TEXT_CACHE:
        # अगर पुराना टेक्स्ट और नया टेक्स्ट बिल्कुल समान है, तो यह केवल रिएक्शन है (इग्नोर करें)
        if MESSAGE_TEXT_CACHE[cache_key] == new_text:
            return

    try:
        await add_chat(message.chat.id)
        user = message.from_user
        if not user: return # सिस्टम मैसेजेस को इग्नोर करें
        
        mention = user.mention
        username = f"@{user.username}" if user.username else "No Username"
        
        text = (
            f"╔══════════════════════╗\n"
            f"   🚨 **𝐄𝐃𝐈𝐓  𝐃𝐄𝐓𝐄𝐂𝐓𝐄𝐃  𝐀𝐋𝐄𝐑𝐓** 🚨\n"
            f"╚══════════════════════╝\n\n"
            f"🚫 **Hey {mention}, Editing messages is strictly**\n"
            f"**prohibited due to copyright & safety!**\n\n"
            f"📝 **User Information:**\n"
            f"  » 👤 **Name:** {mention}\n"
            f"  » 🌐 **Username:** {username}\n"
            f"  » 🆔 **User ID:** `{user.id}`\n\n"
            f"🗑️ `Your original message has been deleted.`\n\n"
            f"⏳ __This warning will auto-delete in 60s.__\n"
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
        
        # मैसेज डिलीट होने पर कैश मेमोरी से साफ़ करें
        MESSAGE_TEXT_CACHE.pop(cache_key, None)
        try:
            CACHE_KEYS_TRACKER.remove(cache_key)
        except ValueError:
            pass
        
        # मैसेज डिलीट करें
        await delete_msg(message)
        
        # वार्निंग भेजें
        warning_msg = await client.send_message(chat_id=message.chat.id, text=text, reply_markup=buttons)
        
        # 60 सेकंड बाद डिलीट करें
        asyncio.create_task(delete_after_delay(warning_msg, 60))
        
    except Exception as e:
        print(f"Edit Handler Error: {e}")

# ==========================================================
# 🚀 CORE ENTRYPOINT
# ==========================================================
async def main():
    threading.Thread(target=run_server, daemon=True).start()
    print("✨ @EditXguardbot is starting up successfully...")
    
    # रॉ अपडेट्स को ट्रैक करने के लिए हुक सेट करें
    @app.on_raw_update()
    async def raw_update_handler(client: Client, update, users, chats):
        if not hasattr(client, "_raw_updates"):
            client._raw_updates = []
        client._raw_updates.append(update)
        # लिस्ट बहुत बड़ी न हो इसलिए आखिरी 10 अपडेट्स ही रखें
        if len(client._raw_updates) > 10:
            client._raw_updates.pop(0)

    await app.start()
    await idle()
    await app.stop()

if __name__ == "__main__":
    loop.run_until_complete(main())
