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

# Admin Telegram ID — yangi arizalar yuboriladigan foydalanuvchi
try:
    ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
except ValueError:
    ADMIN_ID = 0

# Ma'lumotlar bazasi yo'li
DATABASE_PATH = os.getenv("DATABASE_PATH", "bitu.db")

# Universitet bog'lanish ma'lumotlari (yakuniy xabarda ko'rsatiladi)
UNIVERSITY_PHONE = "+998 65 220 00 00"
UNIVERSITY_SITE = "bitu.uz"

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
    if ADMIN_ID == 0:
        raise RuntimeError(
            "ADMIN_ID topilmadi yoki noto'g'ri! .env faylda ADMIN_ID ni belgilang."
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
