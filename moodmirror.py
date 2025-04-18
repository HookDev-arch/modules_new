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

import logging
import random
from .. import loader, utils

__version__ = (1, 0, 5)

logger = logging.getLogger(__name__)

@loader.tds
class MoodMirror(loader.Module):
    """Отражает твое настроение через эмодзи и цитаты"""

    strings = {
        "name": "MoodMirror",
        "mood_detected": "🌟 Твое настроение: {mood}\n{emoji} {quote}",
        "no_mood": "🤔 Я пока не понял твоего настроения. Напиши что-нибудь!",
        "mood_reset": "🧹 Анализ настроения сброшен.",
    }

    strings_ru = {
        "name": "MoodMirror",
        "mood_detected": "🌟 Твое настроение: {mood}\n{emoji} {quote}",
        "no_mood": "🤔 Я пока не понял твоего настроения. Напиши что-нибудь!",
        "mood_reset": "🧹 Анализ настроения сброшен.",
    }

    def __init__(self):
        self.mood_history = []
        self.moods = {
            "радость": {
                "words": [
                    "круто", "класс", "здорово", "супер", "рад", "весело", "ура", "отлично", "праздник", "счастье", "позитив", "восторг", "зашибок", "пушка", "огонь",
                    "бери выше", "взлетаю", "жара", "кайф", "клево", "пипец как круто", "мощь", "ништяк", "просто бомба", "ржака", "супер пупер", "тусня", "флекс",
                    "хайп", "четко", "шик", "эпик", "ясно-понятно", "ахуенно", "блеск", "в кайф", "гуд", "зачет", "збс", "имба", "кек", "лол", "на ура", "пиздец как круто",
                    "с кайфом", "тема", "топчик", "улет", "фуф", "хорош", "чумово", "шок", "эщкере", "бери и делай", "вперед", "газуем", "давай зажжем", "жги",
                    "заруба", "крутан", "летим", "на стиле", "огнище", "погнали", "разрыв", "светим", "тащим", "турбо", "угораем", "фан", "хит", "цепляет", "шпилим",
                    "бери больше", "взрыв мозга", "громко", "движ", "жизнь кипит", "зажгли", "крутой поворот", "на максималках", "просто улет", "рвем", "сносит башню",
                    "трещит", "ууу", "флеш", "хайпово", "чисто кайф", "эмоции через край", "бери и вали", "врубай", "гасим", "докажи", "жги напалмом", "зацени",
                    "круче всех", "на взлете", "просто пушка", "ржачно", "суперская тема", "туса", "фуфел", "хайпим", "четкость", "шикарно", "эпично", "ясен пень",
                    "ахренеть", "блин круто", "в шоке", "гуд вайб", "зачетно", "збс настроение", "имбово", "кекнул", "лол кек", "на ура идет", "пиздец весело",
                    "с кайфушкой", "темка", "топово", "улетно", "фуфырь", "хорошенько", "чумовее некуда", "шок-контент", "эщкере на максимум", "бери и делай красиво",
                    "вперед и с песней", "газ в пол", "давай навали", "жги как надо", "заруливаем", "крутой замес", "летим на всех парах", "на стиле жить",
                    "огни города", "погнали тусить", "разрываем шаблоны", "светимся", "тащим на ура", "турбо-режим", "угораем по полной", "фаново", "хитовый день",
                    "цепляющая штука", "шпили-вили", "бери больше кайфа", "взрывной движ", "громкий старт", "движуха идет", "жизнь на полную", "зажгли по полной",
                    "крутой поворот событий", "на максималках жить", "просто улетный день", "рвем на куски", "сносит крышу", "трещит по швам", "ууу как круто",
                    "флешит", "хайповая тема", "чисто кайфовый день", "эмоции на пределе", "бери и вали на тусу", "врубай на всю", "гасим свет", "докажи что можешь",
                    "жги напалмом братишка", "зацени как круто", "круче всех на районе", "на взлете жить", "просто пушка ган", "ржака полная", "суперская движуха",
                    "туса на миллион", "фуфел полный", "хайпим на всю", "четкость в деле", "шикарный день", "эпичный замес", "ясен пень что круто", "ахренеть как весело",
                    "блин крутой поворот", "в шоке от кайфа", "гуд вайбс только", "зачетный день", "збс все идет", "имбовая тема", "кекнул от радости", "лол кек че за движ",
                    "на ура все тащим", "пиздец как заходит", "с кайфушкой живем", "темка огонь", "топово тащим", "улетный вайб", "фуфырь полный кайф",
                    "хорошенько зажгли", "чумовее всех", "шок-контент на максимум", "эщкере в деле"
                ],
                "emojis": ["😊", "🎉", "🌞", "✨", "🥳"],
                "quotes": [
                    "Счастье — это когда душа танцует!",
                    "Улыбка — твой лучший аксессуар.",
                    "Жизнь прекрасна, когда ты в деле!",
                    "Свети ярче солнца!"
                ]
            },
            "грусть": {
                "words": [
                    "грустно", "плохо", "жаль", "тоска", "печаль", "слезы", "одиноко", "хреново", "упал", "разбит", "все хуйня", "настроение в жопе", "пиздец",
                    "бери и плачь", "в душе дождь", "гасим свет", "день не задался", "жизнь боль", "заебало", "капец", "конец", "лажа", "мрак", "не в кайф",
                    "облом", "пиздец как грустно", "разъеб", "свет потух", "трындец", "уныло", "фуфло", "хана", "чернота", "швах", "все пропало", "грусть тоска",
                    "день в агонии", "жизнь на паузе", "зачем все", "как в тумане", "минус вайб", "на дне", "обида", "плак плак", "разочарование", "скука",
                    "тоскую", "тяжело", "уныние", "фу как плохо", "хмуро", "черный день", "все бесит", "грустный вайб", "день пиздец", "жизнь не та",
                    "заебался грустить", "капец настроению", "конец света", "лажа полная", "мрак в душе", "не в настроении", "облом полный", "пиздец всему",
                    "разъеб в душе", "света нет", "трындец полный", "уныло все", "фуфло день", "хана настроению", "чернота в глазах", "швах полный",
                    "все пропало навсегда", "грусть тоска пиздец", "день в агонии полный", "жизнь на паузе грустно", "зачем все это", "как в тумане жить",
                    "минус вайб полный", "на дне души", "обида на всех", "плак плак в душе", "разочарование полное", "скука смертная", "тоскую по кайфу",
                    "тяжело на душе", "уныние в сердце", "фу как плохо все", "хмуро и тоскливо", "черный день в жизни", "все бесит пиздец", "грустный вайб полный",
                    "день пиздец полный", "жизнь не та что раньше", "заебался грустить совсем", "капец настроению окончательно", "конец света в душе",
                    "лажа полная в жизни", "мрак в душе навсегда", "не в настроении совсем", "облом полный пиздец", "пиздец всему и вся", "разъеб в душе полный",
                    "света нет вообще", "трындец полный в жизни", "уныло все до жопы", "фуфло день полный", "хана настроению навсегда", "чернота в глазах всегда",
                    "швах полный в душе", "все пропало навсегда и точка", "грусть тоска пиздец полный", "день в агонии полный пиздец", "жизнь на паузе грустно навсегда",
                    "зачем все это жить", "как в тумане жить всегда", "минус вайб полный пиздец", "на дне души навсегда", "обида на всех и вся",
                    "плак плак в душе всегда", "разочарование полное в жизни", "скука смертная навсегда", "тоскую по кайфу всегда", "тяжело на душе пиздец",
                    "уныние в сердце навсегда", "фу как плохо все всегда", "хмуро и тоскливо вечно", "черный день в жизни навсегда", "все бесит пиздец полный",
                    "грустный вайб полный пиздец", "день пиздец полный в жизни", "жизнь не та что раньше навсегда", "заебался грустить совсем пиздец",
                    "капец настроению окончательно пиздец", "конец света в душе навсегда", "лажа полная в жизни пиздец", "мрак в душе навсегда пиздец",
                    "не в настроении совсем пиздец", "облом полный пиздец полный", "пиздец всему и вся навсегда", "разъеб в душе полный пиздец",
                    "света нет вообще никогда", "трындец полный в жизни пиздец", "уныло все до жопы пиздец", "фуфло день полный пиздец",
                    "хана настроению навсегда пиздец", "чернота в глазах всегда пиздец", "швах полный в душе пиздец", "все пропало навсегда и точка пиздец",
                    "грусть тоска пиздец полный пиздец", "день в агонии полный пиздец пиздец", "жизнь на паузе грустно навсегда пиздец",
                    "зачем все это жить пиздец", "как в тумане жить всегда пиздец", "минус вайб полный пиздец пиздец", "на дне души навсегда пиздец",
                    "обида на всех и вся пиздец", "плак плак в душе всегда пиздец", "разочарование полное в жизни пиздец", "скука смертная навсегда пиздец",
                    "тоскую по кайфу всегда пиздец", "тяжело на душе пиздец пиздец", "уныние в сердце навсегда пиздец", "фу как плохо все всегда пиздец",
                    "хмуро и тоскливо вечно пиздец", "черный день в жизни навсегда пиздец"
                ],
                "emojis": ["😔", "🌧️", "💧", "🥀", "😢"],
                "quotes": [
                    "Дождь пройдет, и солнце выглянет снова.",
                    "Иногда тишина говорит громче слов.",
                    "Все проходит, и это тоже пройдет.",
                    "Грусть — это тень перед светом."
                ]
            },
            "усталость": {
                "words": [
                    "устал", "выдохся", "спать", "надоело", "лень", "нет сил", "утомился", "выжат", "сонный", "капец", "заебался", "всё достало", "бери и спи",
                    "вялый", "гасну", "день на износ", "жизнь выжала", "засыпаю", "как зомби", "лень двигаться", "мне пиздец", "на пределе", "обессилел",
                    "пиздец устал", "развалился", "сон в глазах", "тухну", "умираю", "фу как лень", "хочу спать", "чувствую пиздец", "энергия на нуле",
                    "бери и лежи", "всё наебнулось", "гасим движ", "день выжал", "жизнь на нуле", "засыпаю на ходу", "как зомби жить", "лень шевелиться",
                    "мне пиздец полный", "на пределе сил", "обессилел совсем", "пиздец усталость", "развалился на куски", "сон в глазах всегда",
                    "тухну потихоньку", "умираю от усталости", "фу как лень всё", "хочу спать пиздец", "чувствую пиздец полный", "энергия на нуле всегда",
                    "бери и лежи дальше", "всё наебнулось окончательно", "гасим движ навсегда", "день выжал до капли", "жизнь на нуле пиздец",
                    "засыпаю на ходу всегда", "как зомби жить каждый день", "лень шевелиться пиздец", "мне пиздец полный пиздец", "на пределе сил всегда",
                    "обессилел совсем пиздец", "пиздец усталость полная", "развалился на куски окончательно", "сон в глазах всегда пиздец",
                    "тухну потихоньку пиздец", "умираю от усталости каждый день", "фу как лень всё пиздец", "хочу спать пиздец полный",
                    "чувствую пиздец полный пиздец", "энергия на нуле всегда пиздец", "бери и лежи дальше пиздец", "всё наебнулось окончательно пиздец",
                    "гасим движ навсегда пиздец", "день выжал до капли пиздец", "жизнь на нуле пиздец пиздец", "засыпаю на ходу всегда пиздец",
                    "как зомби жить каждый день пиздец", "лень шевелиться пиздец пиздец", "мне пиздец полный пиздец пиздец", "на пределе сил всегда пиздец",
                    "обессилел совсем пиздец пиздец", "пиздец усталость полная пиздец", "развалился на куски окончательно пиздец",
                    "сон в глазах всегда пиздец пиздец", "тухну потихоньку пиздец пиздец", "умираю от усталости каждый день пиздец",
                    "фу как лень всё пиздец пиздец", "хочу спать пиздец полный пиздец", "чувствую пиздец полный пиздец пиздец",
                    "энергия на нуле всегда пиздец пиздец", "бери и лежи дальше пиздец пиздец", "всё наебнулось окончательно пиздец пиздец",
                    "гасим движ навсегда пиздец пиздец", "день выжал до капли пиздец пиздец", "жизнь на нуле пиздец пиздец пиздец",
                    "засыпаю на ходу всегда пиздец пиздец", "как зомби жить каждый день пиздец пиздец", "лень шевелиться пиздец пиздец пиздец",
                    "мне пиздец полный пиздец пиздец пиздец", "на пределе сил всегда пиздец пиздец", "обессилел совсем пиздец пиздец пиздец",
                    "пиздец усталость полная пиздец пиздец", "развалился на куски окончательно пиздец пиздец", "сон в глазах всегда пиздец пиздец пиздец",
                    "тухну потихоньку пиздец пиздец пиздец", "умираю от усталости каждый день пиздец пиздец", "фу как лень всё пиздец пиздец пиздец",
                    "хочу спать пиздец полный пиздец пиздец", "чувствую пиздец полный пиздец пиздец пиздец", "энергия на нуле всегда пиздец пиздец пиздец",
                    "бери и лежи дальше пиздец пиздец пиздец", "всё наебнулось окончательно пиздец пиздец пиздец", "гасим движ навсегда пиздец пиздец пиздец",
                    "день выжал до капли пиздец пиздец пиздец", "жизнь на нуле пиздец пиздец пиздец пиздец", "засыпаю на ходу всегда пиздец пиздец пиздец",
                    "как зомби жить каждый день пиздец пиздец пиздец", "лень шевелиться пиздец пиздец пиздец пиздец",
                    "мне пиздец полный пиздец пиздец пиздец пиздец", "на пределе сил всегда пиздец пиздец пиздец", "обессилел совсем пиздец пиздец пиздец пиздец",
                    "пиздец усталость полная пиздец пиздец пиздец", "развалился на куски окончательно пиздец пиздец пиздец",
                    "сон в глазах всегда пиздец пиздец пиздец пиздец", "тухну потихоньку пиздец пиздец пиздец пиздец",
                    "умираю от усталости каждый день пиздец пиздец пиздец", "фу как лень всё пиздец пиздец пиздец пиздец",
                    "хочу спать пиздец полный пиздец пиздец пиздец", "чувствую пиздец полный пиздец пиздец пиздец пиздец",
                    "энергия на нуле всегда пиздец пиздец пиздец пиздец"
                ],
                "emojis": ["😴", "🥱", "🛌", "😩", "💤"],
                "quotes": [
                    "Отдых — это тоже искусство.",
                    "Сон — лучший лекарь.",
                    "Пора дать себе передышку.",
                    "Тишина лечит усталость."
                ]
            },
            "злость": {
                "words": [
                    "бесит", "злюсь", "раздражает", "фу", "достали", "нервы", "беда", "злой", "гнев", "взрыв", "пиздец бесит", "нахуй всё", "ебать как бесит",
                    "бери и пиздец", "всё заебало", "гасим всех", "день пиздец", "жизнь хуйня", "заебали все", "капец нервы", "конец терпению", "лажа бесит",
                    "мрак в голове", "не могу больше", "облом пиздец", "пиздец как раздражает", "разъеб полный", "свет выруби", "трындец нервы",
                    "уныло бесит", "фуфло всё", "хана терпению", "чернота бесит", "швах нервы", "все пиздец достали", "грусть тоска бесит", "день в агонии бесит",
                    "жизнь на паузе бесит", "зачем всё это бесит", "как в тумане бесит", "минус вайб бесит", "на дне бесит", "обида бесит", "плак плак бесит",
                    "разочарование бесит", "скука бесит", "тоскую бесит", "тяжело бесит", "уныние бесит", "фу как плохо бесит", "хмуро бесит", "черный день бесит",
                    "все бесит пиздец", "грустный вайб бесит", "день пиздец бесит", "жизнь не та бесит", "заебался бесить", "капец настроению бесит",
                    "конец света бесит", "лажа полная бесит", "мрак в душе бесит", "не в настроении бесит", "облом полный бесит", "пиздец всему бесит",
                    "разъеб в душе бесит", "света нет бесит", "трындец полный бесит", "уныло всё бесит", "фуфло день бесит", "хана настроению бесит",
                    "чернота в глазах бесит", "швах полный бесит", "все пропало бесит", "грусть тоска пиздец бесит", "день в агонии полный бесит",
                    "жизнь на паузе грустно бесит", "зачем всё это жить бесит", "как в тумане жить бесит", "минус вайб полный бесит", "на дне души бесит",
                    "обида на всех бесит", "плак плак в душе бесит", "разочарование полное бесит", "скука смертная бесит", "тоскую по кайфу бесит",
                    "тяжело на душе бесит", "уныние в сердце бесит", "фу как плохо всё бесит", "хмуро и тоскливо бесит", "черный день в жизни бесит",
                    "все бесит пиздец полный", "грустный вайб полный бесит", "день пиздец полный бесит", "жизнь не та что раньше бесит",
                    "заебался грустить бесит", "капец настроению окончательно бесит", "конец света в душе бесит", "лажа полная в жизни бесит",
                    "мрак в душе навсегда бесит", "не в настроении совсем бесит", "облом полный пиздец бесит", "пиздец всему и вся бесит",
                    "разъеб в душе полный бесит", "света нет вообще бесит", "трындец полный в жизни бесит", "уныло всё до жопы бесит",
                    "фуфло день полный бесит", "хана настроению навсегда бесит", "чернота в глазах всегда бесит", "швах полный в душе бесит",
                    "все пропало навсегда и точка бесит", "грусть тоска пиздец полный бесит", "день в агонии полный пиздец бесит",
                    "жизнь на паузе грустно навсегда бесит", "зачем всё это жить пиздец бесит", "как в тумане жить всегда бесит",
                    "минус вайб полный пиздец бесит", "на дне души навсегда бесит", "обида на всех и вся пиздец бесит", "плак плак в душе всегда бесит",
                    "разочарование полное в жизни пиздец бесит", "скука смертная навсегда бесит", "тоскую по кайфу всегда пиздец бесит",
                    "тяжело на душе пиздец бесит", "уныние в сердце навсегда пиздец бесит", "фу как плохо всё всегда бесит",
                    "хмуро и тоскливо вечно бесит", "черный день в жизни навсегда бесит", "все бесит пиздец полный пиздец",
                    "грустный вайб полный пиздец бесит", "день пиздец полный в жизни бесит", "жизнь не та что раньше навсегда бесит",
                    "заебался грустить совсем пиздец бесит", "капец настроению окончательно пиздец бесит", "конец света в душе навсегда бесит",
                    "лажа полная в жизни пиздец бесит", "мрак в душе навсегда пиздец бесит", "не в настроении совсем пиздец бесит",
                    "облом полный пиздец полный бесит", "пиздец всему и вся навсегда бесит", "разъеб в душе полный пиздец бесит",
                    "света нет вообще никогда бесит", "трындец полный в жизни пиздец бесит", "уныло всё до жопы пиздец бесит",
                    "фуфло день полный пиздец бесит", "хана настроению навсегда пиздец бесит", "чернота в глазах всегда пиздец бесит",
                    "швах полный в душе пиздец бесит", "все пропало навсегда и точка пиздец бесит"
                ],
                "emojis": ["😡", "🔥", "💢", "👿", "😤"],
                "quotes": [
                    "Гнев — это ветер, который гасит свечи разума.",
                    "Выдохни и отпусти.",
                    "Ты сильнее своего раздражения.",
                    "Спокойствие — твой щит."
                ]
            },
            "спокойствие": {
                "words": [
                    "спокойно", "тихо", "мир", "релакс", "хорошо", "уют", "гармония", "баланс", "всё ок", "без паники", "гуд вайб", "дзен", "жизнь течет",
                    "заебок", "кайфуем", "лень в кайф", "мне норм", "на чиле", "отдыхаю", "пиздец как спокойно", "расслабон", "светлый день", "тишина",
                    "успокоился", "фу как хорошо", "хорошо на душе", "чисто релакс", "энергия в балансе", "бери и кайфуй", "всё под контролем", "гасим нервы",
                    "день на чиле", "жизнь в гармонии", "засыпаю спокойно", "как в мечтах", "лень в кайф жить", "мне норм всё", "на чиле на расслабоне",
                    "отдыхаю душой", "пиздец как умиротворенно", "расслабон полный", "светлый день в душе", "тишина в голове", "успокоился наконец",
                    "фу как хорошо всё", "хорошо на душе пиздец", "чисто релакс вайб", "энергия в балансе пиздец", "бери и кайфуй спокойно",
                    "всё под контролем пиздец", "гасим нервы на чиле", "день на чиле пиздец", "жизнь в гармонии пиздец", "засыпаю спокойно пиздец",
                    "как в мечтах жить", "лень в кайф жить пиздец", "мне норм всё пиздец", "на чиле на расслабоне пиздец", "отдыхаю душой пиздец",
                    "пиздец как умиротворенно пиздец", "расслабон полный пиздец", "светлый день в душе пиздец", "тишина в голове пиздец",
                    "успокоился наконец пиздец", "фу как хорошо всё пиздец", "хорошо на душе пиздец пиздец", "чисто релакс вайб пиздец",
                    "энергия в балансе пиздец пиздец", "бери и кайфуй спокойно пиздец", "всё под контролем пиздец пиздец", "гасим нервы на чиле пиздец",
                    "день на чиле пиздец пиздец", "жизнь в гармонии пиздец пиздец", "засыпаю спокойно пиздец пиздец", "как в мечтах жить пиздец",
                    "лень в кайф жить пиздец пиздец", "мне норм всё пиздец пиздец", "на чиле на расслабоне пиздец пиздец", "отдыхаю душой пиздец пиздец",
                    "пиздец как умиротворенно пиздец пиздец", "расслабон полный пиздец пиздец", "светлый день в душе пиздец пиздец",
                    "тишина в голове пиздец пиздец", "успокоился наконец пиздец пиздец", "фу как хорошо всё пиздец пиздец",
                    "хорошо на душе пиздец пиздец пиздец", "чисто релакс вайб пиздец пиздец", "энергия в балансе пиздец пиздец пиздец",
                    "бери и кайфуй спокойно пиздец пиздец", "всё под контролем пиздец пиздец пиздец", "гасим нервы на чиле пиздец пиздец",
                    "день на чиле пиздец пиздец пиздец", "жизнь в гармонии пиздец пиздец пиздец", "засыпаю спокойно пиздец пиздец пиздец",
                    "как в мечтах жить пиздец пиздец", "лень в кайф жить пиздец пиздец пиздец", "мне норм всё пиздец пиздец пиздец",
                    "на чиле на расслабоне пиздец пиздец пиздец", "отдыхаю душой пиздец пиздец пиздец", "пиздец как умиротворенно пиздец пиздец пиздец",
                    "расслабон полный пиздец пиздец пиздец", "светлый день в душе пиздец пиздец пиздец", "тишина в голове пиздец пиздец пиздец",
                    "успокоился наконец пиздец пиздец пиздец", "фу как хорошо всё пиздец пиздец пиздец", "хорошо на душе пиздец пиздец пиздец пиздец",
                    "чисто релакс вайб пиздец пиздец пиздец", "энергия в балансе пиздец пиздец пиздец пиздец",
                    "бери и кайфуй спокойно пиздец пиздец пиздец", "всё под контролем пиздец пиздец пиздец пиздец",
                    "гасим нервы на чиле пиздец пиздец пиздец", "день на чиле пиздец пиздец пиздец пиздец",
                    "жизнь в гармонии пиздец пиздец пиздец пиздец", "засыпаю спокойно пиздец пиздец пиздец пиздец",
                    "как в мечтах жить пиздец пиздец пиздец", "лень в кайф жить пиздец пиздец пиздец пиздец",
                    "мне норм всё пиздец пиздец пиздец пиздец", "на чиле на расслабоне пиздец пиздец пиздец пиздец",
                    "отдыхаю душой пиздец пиздец пиздец пиздец", "пиздец как умиротворенно пиздец пиздец пиздец пиздец",
                    "расслабон полный пиздец пиздец пиздец пиздец", "светлый день в душе пиздец пиздец пиздец пиздец",
                    "тишина в голове пиздец пиздец пиздец пиздец", "успокоился наконец пиздец пиздец пиздец пиздец"
                ],
                "emojis": ["🧘", "🌙", "🌿", "☕", "🌊"],
                "quotes": [
                    "Тишина — это музыка души.",
                    "Спокойствие — сила внутри.",
                    "Мир начинается с тебя.",
                    "Дыши глубже, все в порядке."
                ]
            }
        }

    def analyze_mood(self, text):
        """Анализирует текст и возвращает настроение"""
        text = text.lower()
        for mood, data in self.moods.items():
            if any(word in text for word in data["words"]):
                return mood
        return None

    def get_mood_response(self, mood):
        """Генерирует ответ с эмодзи и цитатой"""
        if mood not in self.moods:
            return None
        data = self.moods[mood]
        emoji = random.choice(data["emojis"])
        quote = random.choice(data["quotes"])
        return {"mood": mood, "emoji": emoji, "quote": quote}

    @loader.watcher("out", only_messages=True)
    async def watcher(self, message):
        """Следит за твоими сообщениями и анализирует настроение"""
        if message.sender_id != (await self._client.get_me()).id:
            return
        mood = self.analyze_mood(message.text)
        if mood:
            self.mood_history.append(mood)
            if len(self.mood_history) > 10:  # Ограничиваем историю
                self.mood_history.pop(0)

    @loader.command(ru_doc="Показать текущее настроение")
    async def mood(self, message):
        """Показывает текущее настроение"""
        if not self.mood_history:
            await utils.answer(message, self.strings["no_mood"])
            return

        # Берем последнее настроение
        latest_mood = self.mood_history[-1]
        response = self.get_mood_response(latest_mood)
        if response:
            await utils.answer(message, self.strings["mood_detected"].format(**response))

    @loader.command(ru_doc="Сбросить анализ настроения")
    async def moodreset(self, message):
        """Сбрасывает историю настроения"""
        self.mood_history = []
        await utils.answer(message, self.strings["mood_reset"])
