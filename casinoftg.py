from telethon import events
from .. import loader, utils

@loader.tds
class ReplyMod(loader.Module):
    """Автоответчик с реакцией 💤 и настраиваемым сообщением в ЛС"""

    strings = {
        "name": "Reply",
        "enabled": "✅ Автоответ включен",
        "disabled": "❌ Автоответ выключен",
        "no_message": "⚠️ Сообщение для ответа не установлено. Используйте `.reply set <текст>`",
        "set_message": "✏️ Сообщение для автоответа установлено:\n{}",
        "usage": "Использование:\n.reply on - включить\n.reply off - выключить\n.reply set <текст> - установить сообщение"
    }

    def __init__(self):
        self.config = {
            "enabled": False,
            "message": None
        }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.config["enabled"] = self.db.get(self.name, "enabled", False)
        self.config["message"] = self.db.get(self.name, "message", None)

    @loader.unrestricted
    async def replycmd(self, message):
        args = utils.get_args_raw(message)
        if not args:
            await message.edit(self.strings["usage"])
            return

        cmd, *text = args.split(" ", 1)
        cmd = cmd.lower()

        if cmd == "on":
            if not self.config["message"]:
                await message.edit(self.strings["no_message"])
                return
            self.config["enabled"] = True
            self.db.set(self.name, "enabled", True)
            await message.edit(self.strings["enabled"])

        elif cmd == "off":
            self.config["enabled"] = False
            self.db.set(self.name, "enabled", False)
            await message.edit(self.strings["disabled"])

        elif cmd == "set":
            if not text:
                await message.edit("⚠️ Укажите сообщение после команды `.reply set`")
                return
            msg = text[0].strip()
            self.config["message"] = msg
            self.db.set(self.name, "message", msg)
            await message.edit(self.strings["set_message"].format(msg))

        else:
            await message.edit(self.strings["usage"])

    @loader.ratelimit
    async def watcher(self, message):
        if not self.config["enabled"]:
            return

        if message.out:
            return

        # Проверяем, что это ЛС
        if not message.is_private:
            return

        if not message.text:
            return

        # Ставим реакцию
        try:
            await message.react("💤")
        except Exception:
            pass

        # Отвечаем текстом
        try:
            await message.reply(self.config["message"])
        except Exception:
            pass