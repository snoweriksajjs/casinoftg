from .. import loader, utils
import asyncio
from telethon.tl.types import PeerUser

@loader.tds
class AutoReplyOnceMod(loader.Module):
    """Автоответ в ЛС + реакция 💤 — только один раз каждому"""

    strings = {"name": "AutoReplyOnce"}

    def __init__(self):
        self.reply_enabled = True
        self.reply_text = "Привет! Я сейчас не могу ответить."
        self.replied_users = set()

    async def watcher(self, message):
        # Не обрабатываем исходящие сообщения и без sender_id
        if message.out or not getattr(message, "sender_id", None):
            return

        # Только личные сообщения (PeerUser)
        if not isinstance(message.to_id, PeerUser):
            return

        if not self.reply_enabled:
            return

        if message.sender_id in self.replied_users:
            return

        try:
            await asyncio.sleep(1)

            # Ставим реакцию
            await message.react("💤")

            # Отправляем ответ
            await message.reply(self.reply_text)

            self.replied_users.add(message.sender_id)
        except Exception as e:
            print(f"[AutoReplyOnce] Ошибка: {e}")

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
        await message.edit("🔄 Список сброшен. Бот снова будет отвечать на первое сообщение.")