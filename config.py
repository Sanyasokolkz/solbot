import os
import json
import pathlib

api_id   = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")          # ← обязательна
admin_id  = int(os.getenv("ADMIN_USER_ID"))

session_name = os.getenv("SESSION_NAME", "railway")

# хранилище каналов
ch_file = pathlib.Path(__file__).with_name(".channels.json")

def load_channels() -> list[str]:
    if ch_file.exists():
        return json.loads(ch_file.read_text())
    # первый запуск – берём из env
    raw = os.getenv("CHANNELS", "")
    return [c.strip() for c in raw.split(",") if c.strip()]

channel_list = load_channels()

def save_channels(chs: list[str]) -> None:
    ch_file.write_text(json.dumps(chs))
    global channel_list
    channel_list[:] = chs
