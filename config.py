# config.py  (bot-версия)
import os

api_id   = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME", "railway")

BOT_TOKEN      = os.getenv("BOT_TOKEN")          # ← обязательно
ADMIN_USER_ID  = int(os.getenv("ADMIN_USER_ID")) # ← ваш ID

# список каналов храним как и раньше
import json, pathlib
CH_FILE = pathlib.Path(__file__).with_name(".channels.json")

def load_channels():
    if CH_FILE.exists():
        return json.loads(CH_FILE.read_text())
    raw = os.getenv("CHANNELS", "")
    return [c.strip() for c in raw.split(",") if c.strip()]

channel_list = load_channels()

def save_channels(chs):
    CH_FILE.write_text(json.dumps(chs))
    global channel_list
    channel_list[:] = chs
