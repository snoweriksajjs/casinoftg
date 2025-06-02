from .. import loader
import asyncio

@loader.tds
class TelegramSlotsMod(loader.Module):
    """Кидает 🎰 до тех пор, пока не выпадет нужный результат"""

    strings = {"name": "RealSlots"}

    async def slotscmd(self, message):
        """Использование: .slots <число от 1 до 6> (например .slots 5 для 777)"""
        args = message.text.split(maxsplit=1)
        if len(args) < 2 or not args[1].isdigit():
            await message.edit("Укажи число от 1 до 6 (1=🍒, 5=777)")
            return

        target = int(args[1])
        if target < 1 or target > 6:
            await message.edit("Допустимые значения: 1–6")
            return

        await message.delete()
        prev_msg = None

        while True:
            if prev_msg:
                try:
                    await prev_msg.delete()
                except:
                    pass

            # Отправляем анимированный 🎰
            dice_msg = await message.client.send_message(message.chat_id, file="🎰")
            await asyncio.sleep(2)  # ждём завершения анимации

            if dice_msg.media and hasattr(dice_msg.media, "value"):
                if dice_msg.media.value == target:
                    break  # Оставляем победное сообщение

            prev_msg = dice_msg
