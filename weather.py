__version__ = (3, 3, 1)

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

def choose_lang(city: str) -> str:
    return "ru" if city and city[0].lower() in rus else "en"

def clean_ascii(raw_text: str) -> str:
    """Очищает ответ wttr.in от Location/Follow и невалидных байтов"""
    raw_text = raw_text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")
    ansi_escape = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")
    raw_text = ansi_escape.sub("", raw_text)

    lines = raw_text.splitlines()
    filtered = [
        l for l in lines
        if l.strip() and not l.startswith("Location:") and not l.startswith("Follow ")
    ]
    return "\n".join(filtered)

def fetch_weather(city: str, lang: str) -> str:
    """Запрашивает короткий ASCII-прогноз с wttr.in"""
    url = f"https://wttr.in/{quote_plus(city)}?0Fqm&lang={lang}&m"
    try:
        r = requests.get(url, timeout=8)
    except requests.RequestException as e:
        return f"⚠ Ошибка запроса: {e}"
    return clean_ascii(r.text)

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
        """Show short ASCII forecast"""
        city = utils.get_args_raw(message) or self.db.get(self.strings["name"], "city", "")
        if not city:
            await utils.answer(message, "<b>🚫 Город не указан</b>")
            return

        lang = choose_lang(city)
        short = fetch_weather(city, lang)

        if not short.strip() or short.startswith("⚠"):
            await utils.answer(message, f"<b>{short or '⚠ Нет данных для этого города'}</b>")
            return

        await utils.answer(message, f"<code>{short}</code>")

    async def weather_inline_handler(self, query: GeekInlineQuery) -> None:
        """Inline search (short ASCII forecast)"""
        args = query.args or self.db.get(self.strings["name"], "city", "")
        if not args:
            return

        lang = choose_lang(args)
        short = fetch_weather(args, lang)

        if not short.strip() or short.startswith("⚠"):
            short = short or "⚠ Нет данных для этого города"

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
