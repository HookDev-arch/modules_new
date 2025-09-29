__version__ = (3, 4, 0)

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
    """Запрашивает короткий ASCII-прогноз с fallback на format=3"""
    try:
        url = f"https://wttr.in/{quote_plus(city)}?0Fqm&lang={lang}&m"
        r = requests.get(url, timeout=8)
        cleaned = clean_ascii(r.text)
        if cleaned.strip():
            return cleaned
    except requests.RequestException as e:
        return f"⚠ Ошибка запроса: {e}"

    # fallback: берем короткую строку format=3
    try:
        r2 = requests.get(f"https://wttr.in/{quote_plus(city)}?format=3&lang={lang}&m", timeout=8)
        txt = r2.text.strip()
        if txt:
            return txt
    except requests.RequestException:
        pass

    return "⚠ Нет данных для этого города"


class WeatherMod(loader.Module):
    """Weather module (short ASCII with fallback)"""

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
        """Show short ASCII forecast (with fallback)"""
        city = utils.get_args_raw(message) or self.db.get(self.strings["name"], "city", "")
        if not city:
            await utils.answer(message, "<b>🚫 Город не указан</b>")
            return

        lang = choose_lang(city)
        result = fetch_weather(city, lang)

        # проверка на пустой или ошибочный ответ
        if not result.strip() or result.startswith("⚠"):
            await utils.answer(message, f"<b>{result}</b>")
            return

        await utils.answer(message, f"<code>{result}</code>")

    async def weather_inline_handler(self, query: GeekInlineQuery) -> None:
        """Inline search (short ASCII with fallback)"""
        args = query.args or self.db.get(self.strings["name"], "city", "")
        if not args:
            return

        lang = choose_lang(args)
        result = fetch_weather(args, lang)
        if not result.strip():
            result = "⚠ Нет данных для этого города"

        await query.answer(
            [
                InlineQueryResultArticle(
                    id=rand(20),
                    title=f"Forecast for {args}",
                    description="Short ASCII forecast",
                    input_message_content=InputTextMessageContent(
                        f"<code>{result}</code>",
                        parse_mode="HTML",
                    ),
                )
            ],
            cache_time=0,
        )
