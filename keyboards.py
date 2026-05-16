"""
Inline va Reply tugmalar.
"""
from __future__ import annotations

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

import locales


# ----- Til tanlash -----

def lang_keyboard() -> InlineKeyboardMarkup:
    """Boshlang'ich til tanlash tugmalari."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🇺🇿 O'zbek tili", callback_data="lang:uz")
    builder.button(text="🇷🇺 Русский язык", callback_data="lang:ru")
    builder.adjust(2)
    return builder.as_markup()


# ----- Boshlash / kirish -----

def start_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Boshlash + til o'zgartirish."""
    builder = InlineKeyboardBuilder()
    builder.button(text=locales.t(lang, "btn_start"), callback_data="begin")
    builder.button(
        text=locales.t(lang, "btn_change_lang"), callback_data="change_lang"
    )
    builder.adjust(1)
    return builder.as_markup()


# ----- Telefon raqam yuborish (Reply) -----

def phone_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """Kontakt yuborish tugmasi."""
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(
            text=locales.t(lang, "btn_send_contact"), request_contact=True
        )
    )
    builder.row(KeyboardButton(text=locales.t(lang, "btn_cancel")))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def remove_keyboard() -> ReplyKeyboardRemove:
    """Reply klaviaturani olib tashlash."""
    return ReplyKeyboardRemove()


# ----- Viloyatlar -----

def regions_keyboard() -> InlineKeyboardMarkup:
    """Viloyatlar ro'yxati — 2 ustunda."""
    builder = InlineKeyboardBuilder()
    for i, region in enumerate(locales.REGIONS):
        builder.button(text=region, callback_data=f"region:{i}")
    builder.adjust(2)
    return builder.as_markup()


# ----- Bosqichlar -----

def levels_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Bakalavr / Magistratura / Klinik ordinatura — 1 ustunda.

    Pastida 🔙 Orqaga — viloyatni qayta tanlash.
    """
    builder = InlineKeyboardBuilder()
    for key, label in locales.LEVELS.items():
        builder.button(text=label, callback_data=f"level:{key}")
    builder.button(text=locales.t(lang, "btn_back"), callback_data="back:region")
    # bosqichlar — har biri alohida qator, oxirida orqaga
    builder.adjust(*([1] * len(locales.LEVELS)), 1)
    return builder.as_markup()


# ----- Yo'nalishlar -----

def directions_keyboard(level_key: str, lang: str = "uz") -> InlineKeyboardMarkup:
    """Bosqichga mos yo'nalishlar — 2 ustunda, callback'da indeks.

    Pastida 🔙 Orqaga — bosqichni qayta tanlash.
    """
    builder = InlineKeyboardBuilder()
    items = locales.directions_for(level_key)
    for i, name in enumerate(items):
        builder.button(text=name, callback_data=f"dir:{i}")
    builder.button(text=locales.t(lang, "btn_back"), callback_data="back:level")
    # yo'nalishlar 2 ustunda, oxirgi qatorda — orqaga (1 ta tugma)
    rows = [2] * ((len(items) + 1) // 2)
    builder.adjust(*rows, 1)
    return builder.as_markup()


# ----- Tasdiqlash -----

def confirm_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Tasdiqlash / qaytadan to'ldirish."""
    builder = InlineKeyboardBuilder()
    builder.button(text=locales.t(lang, "btn_confirm"), callback_data="confirm:yes")
    builder.button(text=locales.t(lang, "btn_retry"), callback_data="confirm:retry")
    builder.adjust(1)
    return builder.as_markup()


# ----- Allaqachon ariza bor -----

def already_applied_keyboard(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=locales.t(lang, "btn_new_application"),
        callback_data="new_application",
    )
    return builder.as_markup()


# ----- Admin: ariza ustida amallar -----

def admin_application_keyboard(app_id: int, telegram_id: int) -> InlineKeyboardMarkup:
    """Admin uchun: bog'lanish + status tugmalari."""
    builder = InlineKeyboardBuilder()
    builder.button(
        text=locales.ADMIN_TEXTS["btn_contact"],
        url=f"tg://user?id={telegram_id}",
    )
    builder.button(
        text=locales.ADMIN_TEXTS["btn_status_contacted"],
        callback_data=f"admin_status:contacted:{app_id}",
    )
    builder.button(
        text=locales.ADMIN_TEXTS["btn_status_accepted"],
        callback_data=f"admin_status:accepted:{app_id}",
    )
    builder.button(
        text=locales.ADMIN_TEXTS["btn_status_rejected"],
        callback_data=f"admin_status:rejected:{app_id}",
    )
    builder.adjust(1, 1, 2)
    return builder.as_markup()
