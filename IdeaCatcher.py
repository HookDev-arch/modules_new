# █████   █████                   █████      ██████████                                                                █████     
#░░███   ░░███                   ░░███      ░░███░░░░███                                                              ░░███      
# ░███    ░███   ██████   ██████  ░███ █████ ░███   ░░███  ██████  █████ █████             ██████   ████████   ██████  ░███████  
# ░███████████  ███░░███ ███░░███ ░███░░███  ░███    ░███ ███░░███░░███ ░░███  ██████████ ░░░░░███ ░░███░░███ ███░░███ ░███░░███ 
# ░███░░░░░███ ░███ ░███░███ ░███ ░██████░   ░███    ░███░███████  ░███  ░███ ░░░░░░░░░░   ███████  ░███ ░░░ ░███ ░░░  ░███ ░███ 
# ░███    ░███ ░███ ░███░███ ░███ ░███░░███  ░███    ███ ░███░░░   ░░███ ███              ███░░███  ░███     ░███  ███ ░███ ░███ 
# █████   █████░░██████ ░░██████  ████ █████ ██████████  ░░██████   ░░█████              ░░████████ █████    ░░██████  ████ █████
#░░░░░   ░░░░░  ░░░░░░   ░░░░░░  ░░░░ ░░░░░ ░░░░░░░░░░    ░░░░░░     ░░░░░                ░░░░░░░░ ░░░░░      ░░░░░░  ░░░░ ░░░░░                                                                                                                                 
# meta developer: @wiley_station
# meta icon: https://example.com/moodmirror_icon.png
# meta banner: https://example.com/moodmirror_banner.png

import logging
import random
import datetime
from hikkatl.tl.functions.channels import CreateChannelRequest
from .. import loader, utils

__version__ = (0, 0, 2)

logger = logging.getLogger(__name__)

@loader.tds
class IdeaCatcher(loader.Module):
    """Ловит и хранит твои идеи с тегами"""

    strings = {
        "name": "IdeaCatcher",
        "idea_added": "💡 Идея записана: {idea}\nТеги: {tags}",
        "no_ideas": "🤔 Пока нет идей. Добавь первую с помощью .idea!",
        "ideas_list": "📜 Твои идеи по тегу #{tag}:\n{ideas}",
    }

    strings_ru = {
        "name": "IdeaCatcher",
        "idea_added": "💡 Идея записана: {idea}\nТеги: {tags}",
        "no_ideas": "🤔 Пока нет идей. Добавь первую с помощью .idea!",
        "ideas_list": "📜 Твои идеи по тегу #{tag}:\n{ideas}",
    }

    def __init__(self):
        self.chat = None
        self.base_tags = ["гениально", "бред", "надо_проверить", "вдохновение", "срочно", "интересно", "задумка"]
        self.context_tags = {
            "работа": ["работа", "проект", "задача", "офис", "код"],
            "отдых": ["отдых", "релакс", "выходные", "сон", "путешествие"],
            "творчество": ["идея", "рисунок", "музыка", "текст", "дизайн"],
            "технологии": ["бот", "программа", "гит", "сервер", "апи"],
            "жизнь": ["день", "план", "цель", "мечта", "время"]
        }

    async def client_ready(self):
        """Создаем группу для хранения идей"""
        try:
            async for dialog in self._client.iter_dialogs():
                if dialog.title == "hikka-ideas":
                    self.chat = dialog.entity
                    break
            if not self.chat:
                chat = await self._client(CreateChannelRequest(
                    title="hikka-ideas",
                    about="Мои идеи, пойманные Hikka",
                    broadcast=False,
                    megagroup=True
                ))
                self.chat = chat.chats[0]
            logger.info(f"Группа для идей: {self.chat.id}")
        except Exception as e:
            logger.error(f"Ошибка при создании группы: {e}")

    def get_tags(self, text):
        """Генерирует теги на основе текста"""
        text = text.lower()
        tags = [random.choice(self.base_tags)]  # Базовый случайный тег

        # Добавляем контекстные теги
        for tag, keywords in self.context_tags.items():
            if any(keyword in text for keyword in keywords):
                tags.append(tag)

        return tags

    @loader.command(ru_doc="Записать идею")
    async def idea(self, message):
        """Записывает новую идею"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Напиши идею после .idea!")
            return

        # Генерируем теги
        tags = self.get_tags(args)
        timestamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        idea_text = f"[{timestamp}] {args} {' '.join(f'#{tag}' for tag in tags)}"

        # Отправляем в группу
        await self._client.send_message(self.chat, idea_text)
        await utils.answer(message, self.strings["idea_added"].format(idea=args, tags=" ".join(f"#{tag}" for tag in tags)))

    @loader.command(ru_doc="Показать идеи по тегу")
    async def ideas(self, message):
        """Показывает идеи по указанному тегу"""
        tag = utils.get_args_raw(message)
        if not tag:
            await utils.answer(message, "Укажи тег после .ideas (например, .ideas гениально)")
            return

        ideas = []
        async for msg in self._client.iter_messages(self.chat, limit=100):
            if f"#{tag}" in msg.text:
                ideas.append(msg.text)

        if not ideas:
            await utils.answer(message, self.strings["no_ideas"])
        else:
            ideas_text = "\n".join(ideas)
            await utils.answer(message, self.strings["ideas_list"].format(tag=tag, ideas=ideas_text))
