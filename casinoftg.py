
from .. import loader
import asyncio
import re

@loader.tds
class SlotMachineMod(loader.Module):
    """Автослоты: удаляет сообщения, пока не выпадет 3 одинаковых для заданного фрукта"""

    strings = {"name": "SlotMachine"}

    async def slotscmd(self, message):
        """Использование: .slots fruit (например .slots 777 или .slots grape)"""
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.edit("Укажи фрукт или символ, например `.slots 777`")
            return

        symbol = args[1]
        chat = message.chat_id
        await message.delete()

        while True:
            slot_msg = await message.client.send_message(chat, f".casino {symbol}")
            await asyncio.sleep(1.0)

            async for msg in message.client.iter_messages(chat, limit=5):
                if msg.text and "🎰" in msg.text:
                    match = re.findall(r"🎰 (.*?) 🎰", msg.raw_text)
                    if match:
                        parts = match[0].split(" ")
                        if len(parts) == 3 and parts[0] == parts[1] == parts[2]:
                            await msg.delete()
                            await slot_msg.delete()
                            return
                    await msg.delete()

            await slot_msg.delete()
