from .. import loader, utils
from telethon.tl.types import Message

@loader.tds
class ReplyMod(loader.Module):
    """Автоответчик в ЛС с реакцией 💤 и настраиваемым текстом"""

    strings = {
        "name": "Reply",
        "enabled": "✅ Автоответчик включён",
        "disabled": "❌ Автоответчик выключен",
        "no_message": "⚠️ Сообщение не задано. Используй `.reply set <текст>`",
        "set_message": "✏️ Установлено сообщение автоответа:\n{}",
        "usage": "Использование:\n.reply on\n.reply off\n.reply set <текст>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("enabled", False, lambda: "Включить автоответчик"),
            loader.ConfigValue("message", "", lambda: "Сообщение автоответа")
        )

    @loader.unrestricted
    async def replycmd(self, message: Message):
        args = utils.get_args_raw(message)

        if not args:
            await message.edit(self.strings("usage"))
            return

        cmd, *rest = args.split(" ", 1)
        cmd = cmd.lower()

        if cmd == "on":
            if not self.config["message"]:
                await message.edit(self.strings("no_message"))
                return
            self.config["enabled"] = True
            await message.edit(self.strings("enabled"))

        elif cmd == "off":
            self.config["enabled"] = False
            await message.edit(self.strings("disabled"))

        elif cmd == "set":
            if not rest:
                await message.edit("⚠️ Укажи сообщение после `.reply set <текст>`")
                return
            msg = rest[0].strip()
            self.config["message"] = msg
            await message.edit(self.strings("set_message").format(msg))

        else:
            await message.edit(self.strings("usage"))

    async def watcher(self, message: Message):
        if (
            not self.config["enabled"]
            or message.out
            or not message.is_private
            or not message.text
        ):
            return

        try:
            await message.react("💤")
        except:
            pass

        try:
            await message.reply(self.config["message"])
        except:
            pass