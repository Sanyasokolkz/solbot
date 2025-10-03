import asyncio
import os
from telethon import TelegramClient, events
from config import (
    api_id, api_hash, session_name,
    channel_list, ADMIN_USER_ID, save_channels
)
from TGparser import find_solana_contract

client = TelegramClient(session_name, api_id, api_hash)

# ---------- отправка контракта ----------
async def send_to_wizard(contract: str) -> None:
    try:
        await client.send_message(os.getenv("WIZARD_CHAT_ID"), contract)
        print(f"✅ Отправлен контракт: {contract}")
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")

# ---------- парсер ----------
@client.on(events.NewMessage(chats=channel_list))
async def handler(event):
    text = event.raw_text
    print(f"\n📩 Сообщение из {event.chat.username or event.chat_id}")
    contract = find_solana_contract(text)
    if contract:
        print(f"✅ Найден контракт: {contract}")
        await send_to_wizard(contract)

# ---------- админ-команды ----------
@client.on(events.NewMessage(pattern=r"^/add\s+(@?\S+)", from_users=ADMIN_USER_ID))
async def add_ch(event):
    ch = event.pattern_match.group(1)
    if ch not in channel_list:
        save_channels(channel_list + [ch])
    await event.reply(f"✅ Добавлен канал {ch}")

@client.on(events.NewMessage(pattern=r"^/del\s+(@?\S+)", from_users=ADMIN_USER_ID))
async def del_ch(event):
    ch = event.pattern_match.group(1)
    if ch in channel_list:
        save_channels([x for x in channel_list if x != ch])
    await event.reply(f"❌ Удалён канал {ch}")

@client.on(events.NewMessage(pattern="^/list$", from_users=ADMIN_USER_ID))
async def list_ch(event):
    await event.reply("📋 Текущие каналы:\n" + "\n".join(channel_list))

# ---------- старт ----------
async def main():
    print("🚀 Слушаем каналы:", ", ".join(channel_list))
    await client.start()
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())