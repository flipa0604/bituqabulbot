"""
Loyihaning umumiy sozlamalari.
.env fayldan o'qiladi.
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# .env faylni yuklash
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Bot tokeni — BotFather'dan olinadi
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

# Adminlar Telegram ID — yangi arizalar yuboriladigan foydalanuvchilar.
# .env'da ikkita variant qo'llab-quvvatlanadi:
#   ADMIN_IDS=6553203791,8670687158   (vergul bilan ajratilgan ro'yxat)
#   ADMIN_ID=6553203791                (eski formatga moslik)
def _parse_admin_ids() -> list[int]:
    raw = os.getenv("ADMIN_IDS", "").strip()
    ids: list[int] = []
    if raw:
        for part in raw.split(","):
            part = part.strip()
            if not part:
                continue
            try:
                ids.append(int(part))
            except ValueError:
                continue
    single = os.getenv("ADMIN_ID", "").strip()
    if single:
        try:
            single_id = int(single)
            if single_id and single_id not in ids:
                ids.append(single_id)
        except ValueError:
            pass
    return ids


ADMIN_IDS: list[int] = _parse_admin_ids()
# Birinchi admin — eski kod bilan moslik uchun (asosiy admin)
ADMIN_ID: int = ADMIN_IDS[0] if ADMIN_IDS else 0

# Ma'lumotlar bazasi yo'li
DATABASE_PATH = os.getenv("DATABASE_PATH", "bitu.db")

# Universitet bog'lanish ma'lumotlari (yakuniy xabarda ko'rsatiladi)
UNIVERSITY_PHONE = "+998 55 305 99 99"
UNIVERSITY_SITE = "bitu.uz"
UNIVERSITY_INSTAGRAM = "https://www.instagram.com/bitu_uz"
UNIVERSITY_TELEGRAM = "https://t.me/bitiinfo"

# Rate limiting — 1 daqiqada maksimal xabar soni
RATE_LIMIT_MAX = 30
RATE_LIMIT_WINDOW = 60  # soniya

# Konfiguratsiya tekshiruvi
def validate_config() -> None:
    """Konfiguratsiya to'g'ri sozlanganini tekshiradi."""
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN topilmadi! .env faylda BOT_TOKEN ni belgilang."
        )
    if not ADMIN_IDS:
        raise RuntimeError(
            "ADMIN_IDS (yoki ADMIN_ID) topilmadi! .env faylda belgilang."
        )


# Logging sozlamalari
def setup_logging() -> None:
    """Logging tizimini sozlaydi — konsol + fayl."""
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    formatter = logging.Formatter(log_format, datefmt=date_format)

    # Konsolga log
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Faylga log
    file_handler = logging.FileHandler(
        BASE_DIR / "bot.log", encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # aiogram'ning juda shovqinli loglarini kamaytirish
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)
