from telethon import events
from .. import loader, utils

@loader.tds
class ReplyMod(loader.Module):
    """Автоответчик в ЛС с реакцией 💤"""

    strings = {
        "name": "Reply",
        "enabled": "✅ Автоответ включен",
        "disabled": "❌ Автоответ выключен",
        "no_message": "⚠️ Сообщение не установлено. .reply set <текст>",
        "set_message": "✏️ Установлено сообщение:\n{}",
        "usage": ".reply on/off/set <текст>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "enabled", False, lambda: "Включить автоответ"
            ),
            loader.ConfigValue(
                "message", "", lambda: "Текст автоответа"
            )
        )

    @loader.unrestricted
    async def replycmd(self, message):
        args = utils.get_args_raw(message)
        if not args:
            return await message.edit(self.strings["usage"])

        cmd, *text = args.split(" ", 1)
        cmd = cmd.lower()

        if cmd == "on":
            if not self.config["message"]:
                return await message.edit(self.strings["no_message"])
            self.config["enabled"] = True
            return await message.edit(self.strings["enabled"])

        elif cmd == "off":
            self.config["enabled"] = False
            return await message.edit(self.strings["disabled"])

        elif cmd == "set" and text:
            msg = text[0]
            self.config["message"] = msg
            return await message.edit(self.strings["set_message"].format(msg))

        else:
            return await message.edit(self.strings["usage"])

    async def watcher(self, message):
        if not self.config["enabled"] or message.out or not message.is_private:
            return
        try:
            await message.react("💤")
        except:
            pass
        try:
            await message.reply(self.config["message"])
        except:
            pass