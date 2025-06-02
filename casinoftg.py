from .. import loader, utils
import asyncio

@loader.tds
class AutoReplyMod(loader.Module):
    """Автоматический ответчик на входящие сообщения"""
    
    strings = {"name": "AutoReply"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("reply_text", "Я сейчас не в сети.", "Сообщение автоответа"),
            loader.ConfigValue("enabled", True, "Включён автоответчик или нет")
        )

    async def watcher(self, message):
        # Только входящие сообщения
        if not self.config["enabled"] or message.out or not message.sender_id:
            return
        
        # Не отвечаем на ботов
        if message.sender.bot:
            return
        
        # Отвечаем с задержкой
        await asyncio.sleep(1)
        await message.reply(self.config["reply_text"])

    async def setreplycmd(self, message):
        """Установить текст автоответа: .setreply <текст>"""
        text = utils.get_args_raw(message)
        if not text:
            await message.edit("Укажи текст: .setreply <текст>")
            return

        self.config["reply_text"] = text
        await message.edit(f"✅ Ответ сохранён: {text}")

    async def autoreplycmd(self, message):
        """Включить/выключить автоответчик: .autoreply on/off"""
        arg = utils.get_args_raw(message).lower()
        if arg not in ["on", "off"]:
            await message.edit("Используй: .autoreply on / off")
            return

        self.config["enabled"] = (arg == "on")
        status = "включён" if self.config["enabled"] else "выключен"
        await message.edit(f"Автоответчик {status}")
