import os

# 🆔 Telegram API Credentials
API_ID = int(os.environ.get("API_ID", "38138069"))
API_HASH = os.environ.get("API_HASH", "2ed313ebcc45cbcf65d1fc736ec71681")

# 🤖 Bot Configuration Tokens
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8785307171:AAE6ox5IfylJONaBDDM0nr8j0clGizreRwI")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "EditXguardbot")

# 👑 Owner / Developer Details
OWNER_ID = int(os.environ.get("OWNER_ID", "7052968393"))  
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "Amrit_lal_chandel")  

# 📢 Channels & Logs Infrastructure
LOG_GROUP = int(os.environ.get("LOG_GROUP", "-1003947649552"))
UPDATE_CH = os.environ.get("UPDATE_CH", "Edit_Guardian_Update")
SUPPORT_CH = os.environ.get("SUPPORT_CH", "Genu_Bot_Support")

# 🖼️ UI Visual Assets
START_IMG = os.environ.get("START_IMG", "https://files.catbox.moe/9eooj2.jpg")

# 📡 Network & Render Port Binding Configuration
PORT = int(os.environ.get("PORT", "8080"))

