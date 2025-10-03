import asyncio
import os
from telethon import TelegramClient, events
from config import (
    api_id, api_hash, bot_token, admin_id,
    channel_list, save_channels
)
from TGparser import find_solana_contract

# 1. создаём клиента, но НЕ стартуем здесь
client = TelegramClient("bot_session", api_id, api_hash)

# -------------- отправка контракта --------------
async def send_to_wizard(contract: str) -> None:
    try:
        await client.send_message(os.getenv("WIZARD_CHAT_ID"), contract)
        print(f"✅ Отправлен контракт: {contract}")
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")

# -------------- парсер --------------
@client.on(events.NewMessage(chats=channel_list))
async def handler(event):
    contract = find_solana_contract(event.raw_text)
    if contract:
        print(f"✅ Найден контракт: {contract}")
        await send_to_wizard(contract)

# -------------- админ-команды --------------
@client.on(events.NewMessage(pattern=r"^/add\s+(@?\S+)", from_users=admin_id))
async def add_ch(event):
    ch = event.pattern_match.group(1)
    if ch not in channel_list:
        save_channels(channel_list + [ch])
    await event.reply(f"✅ Добавлен канал {ch}")

@client.on(events.NewMessage(pattern=r"^/del\s+(@?\S+)", from_users=admin_id))
async def del_ch(event):
    ch = event.pattern_match.group(1)
    if ch in channel_list:
        save_channels([x for x in channel_list if x != ch])
    await event.reply(f"❌ Удалён канал {ch}")

@client.on(events.NewMessage(pattern="^/list$", from_users=admin_id))
async def list_ch(event):
    await event.reply("📋 Текущие каналы:\n" + "\n".join(channel_list))

# -------------- единая точка запуска --------------
async def main():
    # стартуем бота внутри той же корутины
    await client.start(bot_token=bot_token)
    print("🚀 Бот слушает каналы:", ", ".join(map(str, channel_list)))
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
