from .. import loader
import asyncio
import re

@loader.tds
class SlotMachineMod(loader.Module):
    """Автослоты: удаляет сообщения, пока не выпадут 3 одинаковых"""

    strings = {"name": "SlotMachine"}

    SLOT_COMMANDS = [
        "777",
        "grape",
        "bar",
        "slot",
        "dice",
        "money",
        "dollar",
        "gold",
    ]

    async def slotscmd(self, message):
        """Запуск авто-слотов: .slots"""
        chat = message.chat_id
        await message.delete()

        for symbol in self.SLOT_COMMANDS:
            while True:
                slot_msg = await message.client.send_message(chat, f".casino {symbol}")
                await asyncio.sleep(1.2)

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
