__version__ = (3, 0, 0)

# meta developer: @hookdev_arch 
# meta icon: https://example.com/moodmirror_icon.png 
# meta banner: https://i.yapx.ru/Yk4OQ.jpg

# requires: psutil

import contextlib
import os
import platform
import sys
import psutil
import subprocess

from telethon.tl.types import Message
from .. import loader, utils

def bytes_to_megabytes(b: int) -> int:
    return round(b / 1024 / 1024, 1)

def get_cpu_name():
    try:
        return subprocess.check_output("cat /proc/cpuinfo | grep 'model name' | uniq", shell=True).decode().split(': ')[1].strip()
    except:
        return "n/a"

def get_ram_type():
    try:
        # This works on most Linux systems with dmidecode installed
        return subprocess.check_output("sudo dmidecode --type 17 | grep 'Type:' | head -1", shell=True).decode().split(': ')[1].strip()
    except:
        return "n/a"

def get_disk_info():
    try:
        usage = psutil.disk_usage('/')
        total = round(usage.total / 1024 / 1024 / 1024, 1)
        used = round(usage.used / 1024 / 1024 / 1024, 1)
        free = round(usage.free / 1024 / 1024 / 1024, 1)
        return f"{used}GB / {total}GB (Free: {free}GB)"
    except:
        return "n/a"

@loader.tds
class serverInfoMod(loader.Module):
    """Show server info"""
    strings = {
        "name": "ServerInfo",
        "loading": "<emoji document_id=5271897426117009417>\ud83d\ude98</emoji> <b>Loading server info...</b>",
        "servinfo": (
            "<emoji document_id=5271897426117009417>\ud83d\ude98</emoji> <b>Server Info</b>:\n\n"
            "<emoji document_id=5172854840321114816>\ud83d\udcbb</emoji> <b>CPU:</b> {cpu_name} ({cpu} cores, {cpu_load}%)\n"
            "<emoji document_id=5174693704799093859>\ud83d\udcbb</emoji> <b>RAM:</b> {ram} / {ram_load_mb}MB ({ram_load}%), DDR Type: {ram_type}\n"
            "<emoji document_id=5172839378438849164>\ud83d\udcbb</emoji> <b>Disk:</b> {disk}\n\n"
            "<emoji document_id=5172474181664637769>\ud83d\udcbb</emoji> <b>Kernel:</b> {kernel}\n"
            "{arch_emoji} <b>Arch:</b> {arch}\n"
            "<emoji document_id=5172622400986022463>\ud83d\udcbb</emoji> <b>OS:</b> {os}\n\n"
            "<emoji document_id=5172839378438849164>\ud83d\udcbb</emoji> <b>Python:</b> {python}"
        ),
    }

    strings_ru = {
        "loading": "<emoji document_id=5271897426117009417>\ud83d\ude98</emoji> <b>Загрузка информации о сервере...</b>",
        "servinfo": (
            "<emoji document_id=5271897426117009417>\ud83d\ude98</emoji> <b>Информация о сервере</b>:\n\n"
            "<emoji document_id=5172854840321114816>\ud83d\udcbb</emoji> <b>Процессор:</b> {cpu_name} ({cpu} ядер, {cpu_load}%)\n"
            "<emoji document_id=5174693704799093859>\ud83d\udcbb</emoji> <b>ОЗУ:</b> {ram} / {ram_load_mb}MB ({ram_load}%), Тип: {ram_type}\n"
            "<emoji document_id=5172839378438849164>\ud83d\udcbb</emoji> <b>Диск:</b> {disk}\n\n"
            "<emoji document_id=5172474181664637769>\ud83d\udcbb</emoji> <b>Ядро:</b> {kernel}\n"
            "{arch_emoji} <b>Архитектура:</b> {arch}\n"
            "<emoji document_id=5172622400986022463>\ud83d\udcbb</emoji> <b>ОС:</b> {os}\n\n"
            "<emoji document_id=5172839378438849164>\ud83d\udcbb</emoji> <b>Python:</b> {python}"
        ),
        "_cls_doc": "Показывает информацию о сервере",
    }

    @loader.command(ru_doc="Показать информацию о сервере")
    async def serverinfo(self, message: Message):
        message = await utils.answer(message, self.strings("loading"))

        inf = {
            "cpu": psutil.cpu_count(logical=True) or "n/a",
            "cpu_load": psutil.cpu_percent() or "n/a",
            "ram": bytes_to_megabytes(psutil.virtual_memory().used) or "n/a",
            "ram_load_mb": bytes_to_megabytes(psutil.virtual_memory().total) or "n/a",
            "ram_load": psutil.virtual_memory().percent or "n/a",
            "kernel": utils.escape_html(platform.release()),
            "arch": utils.escape_html(platform.architecture()[0]),
            "os": utils.escape_html(platform.platform()),
            "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "arch_emoji": "<emoji document_id=5172881503478088537>\ud83d\udcbb</emoji>" if "64" in platform.architecture()[0] else "<emoji document_id=5174703196676817427>\ud83d\udcbb</emoji>",
            "cpu_name": get_cpu_name(),
            "ram_type": get_ram_type(),
            "disk": get_disk_info(),
        }

        await utils.answer(message, self.strings("servinfo").format(**inf))
