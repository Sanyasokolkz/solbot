import os
import json
import pathlib

api_id   = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME", "railway")

ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID"))   # ваша цифра

# файл-хранилище каналов (внутри контейнера)
CH_FILE = pathlib.Path(__file__).with_name(".channels.json")

def load_channels() -> list[str]:
    if CH_FILE.exists():
        return json.loads(CH_FILE.read_text())
    # первый запуск – берём из env
    raw = os.getenv("CHANNELS", "")
    return [c.strip() for c in raw.split(",") if c.strip()]

channel_list = load_channels()

def save_channels(chs: list[str]) -> None:
    CH_FILE.write_text(json.dumps(chs))
    global channel_list
    channel_list[:] = chs