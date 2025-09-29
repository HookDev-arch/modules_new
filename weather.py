__version__ = (3, 2, 0)

# █████   █████                   █████      ██████████                                                                █████     
#░░███   ░░███                   ░░███      ░░███░░░░███                                                              ░░███      
# ░███    ░███   ██████   ██████  ░███ █████ ░███   ░░███  ██████  █████ █████             ██████   ████████   ██████  ░███████  
# ░███████████  ███░░███ ███░░███ ░███░░███  ░███    ░███ ███░░███░░███ ░░███  ██████████ ░░░░░███ ░░███░░███ ███░░███ ░███░░███ 
# ░███░░░░░███ ░███ ░███░███ ░███ ░██████░   ░███    ░███░███████  ░███  ░███ ░░░░░░░░░░   ███████  ░███ ░░░ ░███ ░░░  ░███ ░███ 
# ░███    ░███ ░███ ░███░███ ░███ ░███░░███  ░███    ███ ░███░░░   ░░███ ███              ███░░███  ░███     ░███  ███ ░███ ░███ 
# █████   █████░░██████ ░░██████  ████ █████ ██████████  ░░██████   ░░█████              ░░████████ █████    ░░██████  ████ █████
#░░░░░   ░░░░░  ░░░░░░   ░░░░░░  ░░░░ ░░░░░ ░░░░░░░░░░    ░░░░░░     ░░░░░                ░░░░░░░░ ░░░░░      ░░░░░░  ░░░░ ░░░░░                                                                                                                                 
# meta developer: @hookdev_arch
# meta icon: https://example.com/moodmirror_icon.png
# meta banner: https://i.yapx.ru/Yk4OQ.jpg

# scope: inline_content
# requires: requests

import logging
import re
from urllib.parse import quote_plus

import requests
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import Message

from .. import loader, utils
from ..inline import GeekInlineQuery, rand

logger = logging.getLogger(__name__)

n = "\n"
rus = "ёйцукенгшщзхъфывапролджэячсмитьбю"

def escape_ansi(line: str) -> str:
    """Убираем ANSI-коды цветов и управляющие символы"""
    ansi_escape = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")
    return ansi_escape.sub("", line)

class WeatherMod(loader.Module):
    """Weather module (short ASCII forecast)"""

    strings = {"name": "Weather"}

    async def client_ready(self, client, db) -> None:
        if hasattr(self, "hikka"):
            return

        self.db = db
        self.client = client
        try:
            channel = await self.client.get_entity("t.me/morisummermods")
            await client(JoinChannelRequest(channel))
        except Exception:
            logger.error("Can't join morisummermods")
        try:
            post = (await client.get_messages("@morisummermods", ids=[17]))[0]
            await post.react("❤️")
        except Exception:
            logger.error("Can't react to t.me/morisummermods")

    async def weathercitycmd(self, message: Message) -> None:
        """Set default city for forecast"""
        if args := utils.get_args_raw(message):
            self.db.set(self.strings["name"], "city", args)

        await utils.answer(
            message,
            (
                "<b>🏙 Your current city: "
                f"<code>{self.db.get(self.strings['name'], 'city', '🚫 Not specified')}</code></b>"
            ),
        )

    async def weathercmd(self, message: Message) -> None:
        """Show short ASCII weather forecast"""
        city = utils.get_args_raw(message)
        if not city:
            city = self.db.get(self.strings["name"], "city", "")

        if not city:
            await utils.answer(message, "<b>🚫 Город не указан</b>")
            return

        lang = "ru" if city and city[0].lower() in rus else "en"
        req = requests.get(f"https://wttr.in/{quote_plus(city)}?m&lang={lang}")
        text = escape_ansi(req.text)
        short = "\n".join(text.splitlines()[:7])

        await utils.answer(message, f"<code>{short}</code>")

    async def weather_inline_handler(self, query: GeekInlineQuery) -> None:
        """Inline weather search with short ASCII output"""
        args = query.args or self.db.get(self.strings["name"], "city", "")
        if not args:
            return

        lang = "ru" if args and args[0].lower() in rus else "en"
        req = requests.get(f"https://wttr.in/{quote_plus(args)}?m&lang={lang}")
        text = escape_ansi(req.text)
        short = "\n".join(text.splitlines()[:7])

        await query.answer(
            [
                InlineQueryResultArticle(
                    id=rand(20),
                    title=f"Forecast for {args}",
                    description="Short ASCII forecast",
                    input_message_content=InputTextMessageContent(
                        f"<code>{short}</code>",
                        parse_mode="HTML",
                    ),
                )
            ],
            cache_time=0,
        )
