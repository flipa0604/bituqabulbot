"""
Foydalanuvchi kiritmalarini tekshirish.
"""
from __future__ import annotations

import re

# Telefon raqam regexi — +998 bilan boshlanadi, jami 12 ta raqam.
# Probel, qavs va tire ruxsat etiladi.
_PHONE_RE = re.compile(r"^\+?998[\s\-\(\)]*\d{2}[\s\-\(\)]*\d{3}[\s\-\(\)]*\d{2}[\s\-\(\)]*\d{2}$")

# Ism-familiya: harflar (kirill + lotin + o'zbek harflari) va bo'shliq, defis, apostrof
_NAME_RE = re.compile(r"^[A-Za-zА-Яа-яЁёҲҳҚқҒғЎўЪъ'`’\-\s]+$")


def validate_full_name(text: str) -> str | None:
    """Ism-familiyani tekshiradi.

    Qaytaradi: tozalangan matn yoki None (xato).
    """
    if not text:
        return None
    cleaned = " ".join(text.strip().split())
    if len(cleaned) < 4:
        return None
    parts = cleaned.split(" ")
    if len(parts) < 2:
        return None
    if not _NAME_RE.match(cleaned):
        return None
    return cleaned


def normalize_phone(text: str) -> str | None:
    """Telefon raqamni tekshiradi va standart formatga keltiradi.

    Standart format: +998 XX XXX XX XX
    Qaytaradi: formatlangan raqam yoki None.
    """
    if not text:
        return None

    raw = text.strip()
    # 998 bilan boshlanmagan bo'lsa, qo'shamiz (masalan, 90 123 45 67)
    digits_only = re.sub(r"\D", "", raw)
    if len(digits_only) == 9 and digits_only.startswith(("9", "3", "7", "8")):
        digits_only = "998" + digits_only

    if len(digits_only) != 12 or not digits_only.startswith("998"):
        # asl matnda regex orqali ham tekshirib ko'ramiz
        if not _PHONE_RE.match(raw):
            return None
        digits_only = re.sub(r"\D", "", raw)
        if len(digits_only) != 12:
            return None

    # Formatlash: +998 XX XXX XX XX
    return (
        f"+{digits_only[:3]} {digits_only[3:5]} "
        f"{digits_only[5:8]} {digits_only[8:10]} {digits_only[10:12]}"
    )
