import os
import json
import pathlib
import base64

# Telegram API
api_id   = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
admin_id = int(os.getenv("ADMIN_USER_ID"))   # ваш ID

session_name = os.getenv("SESSION_NAME", "railway")

# восстанавливаем session-файл из base64
session_file = pathlib.Path(__file__).with_name(session_name + ".session")
b64 = os.getenv("SESSION_BASE64", "")
if b64 and not session_file.exists():
    session_file.write_bytes(base64.b64decode(b64))

# хранилище каналов
ch_file = pathlib.Path(__file__).with_name(".channels.json")
name_file = pathlib.Path(__file__).with_name(".names.json")

def load_channels() -> list[int]:
    if ch_file.exists():
        return json.loads(ch_file.read_text())
    raw = os.getenv("CHANNELS", "")
    return [int(c.strip()) for c in raw.split(",") if c.strip().isdigit()]

def load_names() -> dict[int, str]:
    return json.loads(name_file.read_text()) if name_file.exists() else {}

channel_list = load_channels()
channel_names = load_names()

def save_channels(chs: list[int]) -> None:
    ch_file.write_text(json.dumps(chs))
    global channel_list
    channel_list[:] = chs

def save_names(names: dict[int, str]) -> None:
    name_file.write_text(json.dumps(names, ensure_ascii=False))
    global channel_names
    channel_names = names
