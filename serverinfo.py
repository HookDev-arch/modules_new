__version__ = (3, 1, 1)

# meta developer: @hookdev_arch 
# meta icon: https://example.com/moodmirror_icon.png 
# meta banner: https://i.yapx.ru/Yk4OQ.jpg

# requires: psutil

import contextlib
import os
import platform
import sys

import psutil
from telethon.tl.types import Message

from .. import loader, utils


def bytes_to_megabytes(b: int) -> int:
    return round(b / 1024 / 1024, 1)


@loader.tds
class serverInfoMod(loader.Module):
    """Show server info"""

    strings = {
        "name": "ServerInfo",
        "loading": (
            "<emoji document_id=5271897426117009417>🚘</emoji> <b>Loading server info...</b>"
        ),
        "servinfo": (
            "<emoji document_id=5271897426117009417>🚘</emoji> <b>Server Info</b>:\n\n"
            "<emoji document_id=5172854840321114816>💻</emoji> <b>CPU:</b> {cpu} Cores {cpu_load}%\n"
            "<emoji document_id=5174693704799093859>💻</emoji> <b>RAM:</b> {ram} / {ram_load_mb}MB ({ram_load}%)\n\n"
            "{gpu_info}\n\n"
            "<emoji document_id=5172474181664637769>💻</emoji> <b>Kernel:</b> {kernel}\n"
            "{arch_emoji} <b>Arch:</b> {arch}\n"
            "<emoji document_id=5172622400986022463>💻</emoji> <b>OS:</b> {os}\n\n"
            "<emoji document_id=5172839378438849164>💻</emoji> <b>Python:</b> {python}"
        ),
    }

    strings_ru = {
        "loading": (
            "<emoji document_id=5271897426117009417>🚘</emoji> <b>Загрузка информации о сервере...</b>"
        ),
        "servinfo": (
            "<emoji document_id=5271897426117009417>🚘</emoji> <b>Информация о сервере</b>:\n\n"
            "<emoji document_id=5172854840321114816>💻</emoji> <b>ЦПУ:</b> {cpu} ядер(-ро) {cpu_load}%\n"
            "<emoji document_id=5174693704799093859>💻</emoji> <b>ОЗУ:</b> {ram} / {ram_load_mb}MB ({ram_load}%)\n\n"
            "{gpu_info}\n\n"
            "<emoji document_id=5172474181664637769>💻</emoji> <b>Ядро:</b> {kernel}\n"
            "{arch_emoji} <b>Архитектура:</b> {arch}\n"
            "<emoji document_id=5172622400986022463>💻</emoji> <b>СО:</b> {os}\n\n"
            "<emoji document_id=5172839378438849164>💻</emoji> <b>Python:</b> {python}"
        ),
        "_cls_doc": "Показывает информацию о сервере",
    }

    @loader.command(ru_doc="Показать информацию о сервере")
    async def serverinfo(self, message: Message):
        """Show server info"""
        message = await utils.answer(message, self.strings("loading"))

        inf = {
            "cpu": "n/a",
            "cpu_load": "n/a",
            "ram": "n/a",
            "ram_load_mb": "n/a",
            "ram_load": "n/a",
            "kernel": "n/a",
            "arch_emoji": "n/a",
            "arch": "n/a",
            "os": "n/a",
            "python": "n/a",
            "gpu_info": (
                "<emoji document_id=5172854840321114816>💻</emoji> <b>GPU:</b> NVIDIA GeForce RTX 4060 Ti\n"
                "<emoji document_id=5172854840321114816>🛆</emoji> <b>Driver:</b> 32.0.15.8088 (27.07.2025)\n"
                "<emoji document_id=5172854840321114816>🎮</emoji> <b>DirectX:</b> 12 (FL 12.1)\n"
                "<emoji document_id=5172854840321114816>🪠</emoji> <b>VRAM Used:</b> 1.4 / 8.0 GB\n"
                "<emoji document_id=5172854840321114816>🔁</emoji> <b>Shared:</b> 0.1 / 15.9 GB\n"
                "<emoji document_id=5172854840321114816>🪠</emoji> <b>Total:</b> 1.5 / 23.9 GB"
            ),
        }

        with contextlib.suppress(Exception):
            inf["cpu"] = psutil.cpu_count(logical=True)

        with contextlib.suppress(Exception):
            inf["cpu_load"] = psutil.cpu_percent()

        with contextlib.suppress(Exception):
            inf["ram"] = bytes_to_megabytes(
                psutil.virtual_memory().total - psutil.virtual_memory().available
            )

        with contextlib.suppress(Exception):
            inf["ram_load_mb"] = bytes_to_megabytes(psutil.virtual_memory().total)

        with contextlib.suppress(Exception):
            inf["ram_load"] = psutil.virtual_memory().percent

        with contextlib.suppress(Exception):
            inf["kernel"] = utils.escape_html(platform.release())

        with contextlib.suppress(Exception):
            inf["arch"] = utils.escape_html(platform.architecture()[0])

        inf["arch_emoji"] = (
            "<emoji document_id=5172881503478088537>💻</emoji>"
            if "64" in (inf.get("arch", "") or "")
            else "<emoji document_id=5174703196676817427>💻</emoji>"
        )

        with contextlib.suppress(Exception):
            system = os.popen("cat /etc/*release").read()
            b = system.find('DISTRIB_DESCRIPTION="') + 21
            system = system[b : system.find('"', b)]
            inf["os"] = utils.escape_html(system)

        with contextlib.suppress(Exception):
            inf["python"] = (
                f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            )

        await utils.answer(message, self.strings("servinfo").format(**inf))
