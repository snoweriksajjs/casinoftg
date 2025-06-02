from .. import loader, utils
import asyncio

@loader.tds
class AutoReplyMod(loader.Module):
    """Простой автоответчик"""

    strings = {"name": "AutoReply"}

    def __init__(self):
        self.reply_enabled = True
        self.reply_text = "Я сейчас не в сети."

    async def watcher(self, message):
        if not self.reply_enabled:
            return
        if message.out or not message.sender_id:
            return
        if message.sender.bot:
            return

        await asyncio.sleep(1)
        try:
            await message.reply(self.reply_text)
        except:
            pass

    async def setreplycmd(self, message):
        """Установить текст автоответа: .setreply <текст>"""
        text = utils.get_args_raw(message)
        if not text:
            await message.edit("Укажи текст: .setreply <текст>")
            return
        self.reply_text = text
        await message.edit(f"✅ Новый автоответ: {text}")

    async def autoreplycmd(self, message):
        """Включить или выключить автоответ: .autoreply on/off"""
        arg = utils.get_args_raw(message).lower()
        if arg not in ["on", "off"]:
            await message.edit("Используй: .autoreply on / off")
            return
        self.reply_enabled = (arg == "on")
        status = "включён" if self.reply_enabled else "выключен"
        await message.edit(f"Автоответчик {status}")