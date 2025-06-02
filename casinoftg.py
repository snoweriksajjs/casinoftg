from .. import loader
import asyncio

@loader.tds
class TelegramSlotsMod(loader.Module):
    """Авто-🎰: кидает слот, пока не выпадет нужный символ"""

    strings = {"name": "RealSlots"}

    # Соответствие: имя → значение Telegram dice
    fruit_map = {
        "cherry": 1,
        "lemon": 2,
        "orange": 3,
        "grape": 4,
        "777": 5,
        "star": 6
    }

    async def slotscmd(self, message):
        """Использование: .slots <название или цифра от 1 до 6>
        Примеры: .slots 777, .slots grape, .slots 5
        """
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.edit("Укажи: .slots <фрукт или число>\nПример: .slots grape или .slots 5")
            return

        target_raw = args[1].lower()

        # Определяем нужный value
        if target_raw.isdigit():
            target_value = int(target_raw)
        else:
            target_value = self.fruit_map.get(target_raw)

        if target_value not in range(1, 7):
            await message.edit("Неверный символ. Используй: cherry, lemon, orange, grape, 777, star или 1–6")
            return

        await message.delete()
        prev_msg = None

        while True:
            # Удаляем прошлый бросок
            if prev_msg:
                try:
                    await prev_msg.delete()
                except:
                    pass

            # Кидаем настоящий слот 🎰
            dice_msg = await message.client.send_message(message.chat_id, file="🎰")
            await asyncio.sleep(2)  # ждём анимацию

            if dice_msg.media and hasattr(dice_msg.media, "value"):
                if dice_msg.media.value == target_value:
                    break  # Успех — оставляем сообщение

            prev_msg = dice_msg
