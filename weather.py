__version__ = (1, 3, 0)

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
    """Убираем цветовые коды из ASCII"""
    ansi_escape = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")
    return ansi_escape.sub("", line)

def clean_ascii(raw_text: str) -> str:
    """Чистим ответ wttr.in от Location и Follow"""
    lines = escape_ansi(raw_text).splitlines()
    filtered = [
        l for l in lines
        if l.strip() and not l.startswith("Location:") and not l.startswith("Follow ")
    ]
    return "\n".join(filtered)

def choose_lang(city: str) -> str:
    return "ru" if city and city[0].lower() in rus else "en"

class WeatherMod(loader.Module):
    """Weather module (short ASCII only)"""

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
        """Show short ASCII forecast (no location leak)"""
        city = utils.get_args_raw(message) or self.db.get(self.strings["name"], "city", "")
        if not city:
            await utils.answer(message, "<b>🚫 Город не указан</b>")
            return

        lang = choose_lang(city)
        url = f"https://wttr.in/{quote_plus(city)}?0Fqm&lang={lang}&m"
        req = requests.get(url, timeout=8)
        short = clean_ascii(req.text)
        await utils.answer(message, f"<code>{short}</code>")

    async def weather_inline_handler(self, query: GeekInlineQuery) -> None:
        """Inline search (short ASCII forecast)"""
        args = query.args or self.db.get(self.strings["name"], "city", "")
        if not args:
            return

        lang = choose_lang(args)
        url = f"https://wttr.in/{quote_plus(args)}?0Fqm&lang={lang}&m"
        req = requests.get(url, timeout=8)
        short = clean_ascii(req.text)

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
