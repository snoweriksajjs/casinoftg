from .. import loader, utils
import asyncio
from telethon.tl.types import PeerUser

@loader.tds
class replyMod(loader.Module):
    """Автоответ в ЛС + реакция 💤 — только один раз каждому"""

    strings = {"name": "reply"}

    def __init__(self):
        self.reply_enabled = True
        self.reply_text = "Привет! Я сейчас не могу ответить."
        self.replied_users = set()

    async def watcher(self, message):
        if not self.reply_enabled:
            return

        if message.out:
            return

        if not message.is_private:
            return

        sender = await message.get_sender()
        if sender.bot or sender.system:
            return

        if message.sender_id in self.replied_users:
            return

        try:
            await asyncio.sleep(1)
            await message.react("💤")
            await message.reply(self.reply_text)
            self.replied_users.add(message.sender_id)
        except Exception as e:
            pass  # Можно заменить на print(str(e)) для отладки

    async def setreplycmd(self, message):
        """Установить текст автоответа: .setreply <текст>"""
        text = utils.get_args_raw(message)
        if not text:
            await message.edit("Укажи текст: .setreply <текст>")
            return
        self.reply_text = text
        await message.edit(f"✅ Новый автоответ: {text}")

    async def autoreplycmd(self, message):
        """Вкл/выкл автоответ: .autoreply on/off"""
        arg = utils.get_args_raw(message).lower()
        if arg == "on":
            self.reply_enabled = True
            await message.edit("✅ Автоответ включён")
        elif arg == "off":
            self.reply_enabled = False
            await message.edit("❌ Автоответ выключен")
        else:
            await message.edit("Используй: .autoreply on / off")

    async def resetreplycmd(self, message):
        """Сбросить список пользователей, которым уже отвечали"""
        self.replied_users.clear()
        await message.edit("🔄 Список сброшен.")