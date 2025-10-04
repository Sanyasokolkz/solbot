import asyncio
import os
from telethon import TelegramClient, events
from config import (
    api_id, api_hash, admin_id,
    channel_list, channel_names, save_channels, save_names
)
from TGparser import find_solana_contract

# user-session (файл уже восстановлен из base64)
client = TelegramClient("railway", api_id, api_hash)

# -------------- отправка контракта --------------
async def send_to_wizard(contract: str, source: str) -> None:
    try:
        msg = f"{contract}\n👁️ Источник: {source}"
        await client.send_message(os.getenv("WIZARD_CHAT_ID"), msg)
        print(f"✅ Отправлен контракт: {contract}  из {source}")
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")

# -------------- парсер каналов --------------
@client.on(events.NewMessage(chats=channel_list))
async def handler(event):
    contract = find_solana_contract(event.raw_text)
    if contract:
        source = channel_names.get(event.chat_id, str(event.chat_id))
        print(f"✅ Найден контракт: {contract}  из {source}")
        await send_to_wizard(contract, source)

# -------------- админ-команды --------------
@client.on(events.NewMessage(pattern=r"^/add\s+(@?\S+)\s+(.+)", from_users=admin_id))
async def add_ch(event):
    ident, name = event.pattern_match.group(1, 2)
    ch_id = int(ident) if ident.isdigit() else (await client.get_entity(ident)).id
    if ch_id not in channel_list:
        save_channels(channel_list + [ch_id])
    channel_names[ch_id] = name
    save_names(channel_names)
    await event.reply(f"✅ Добавлен канал {name} (`{ch_id}`)")

@client.on(events.NewMessage(pattern=r"^/del\s+(@?\S+)", from_users=admin_id))
async def del_ch(event):
    ident = event.pattern_match.group(1)
    ch_id = int(ident) if ident.isdigit() else (await client.get_entity(ident)).id
    if ch_id in channel_list:
        save_channels([x for x in channel_list if x != ch_id])
        channel_names.pop(ch_id, None)
        save_names(channel_names)
    await event.reply(f"❌ Удалён канал `{ch_id}`")

@client.on(events.NewMessage(pattern="^/list$", from_users=admin_id))
async def list_ch(event):
    if not channel_list:
        await event.reply("📋 Список каналов пуст.")
        return
    text = "\n".join(f"{channel_names.get(ch, ch)}  (`{ch}`)" for ch in channel_list)
    await event.reply("📋 Текущие каналы:\n" + text)

# -------------- запуск --------------
async def main():
    await client.start()                       # user-session, phone не спрашивается
    print("🚀 User-бот слушает каналы:", ", ".join(map(str, channel_list)))
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
