"""
Anketa to'ldirish — FSM bilan har bir qadam alohida state.
"""
from __future__ import annotations

import logging
from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import config
import keyboards
import locales
from database import Database
from states import Registration
from utils.validators import normalize_phone, validate_full_name

logger = logging.getLogger(__name__)
router = Router(name="registration")


async def _lang(state: FSMContext, db: Database, user_id: int) -> str:
    """State'dan tilni o'qiydi, bo'lmasa DB'dan."""
    data = await state.get_data()
    lang = data.get("language")
    if lang:
        return lang
    return await db.get_user_language(user_id) or "uz"


# ----- 1) Boshlash tugmasi: ism familiya so'rash -----

@router.callback_query(F.data == "begin")
async def begin_registration(
    call: CallbackQuery, state: FSMContext, db: Database
) -> None:
    """Anketa boshlandi — ism familiya so'rash."""
    try:
        lang = await _lang(state, db, call.from_user.id)
        await state.set_state(Registration.full_name)
        await call.message.edit_text(locales.t(lang, "ask_full_name"))
        await call.answer()
    except Exception:
        logger.exception("begin_registration xatosi")
        await call.answer(locales.t("uz", "error_generic"), show_alert=True)


# ----- 2) Ism familiya qabul qilish -----

@router.message(StateFilter(Registration.full_name), F.text)
async def on_full_name(
    message: Message, state: FSMContext, db: Database
) -> None:
    lang = await _lang(state, db, message.from_user.id)

    # Cancel tugmasi yoki /cancel kabi matnlar — bekor qilish
    if message.text.strip().lower() in {"/cancel", "❌ bekor qilish", "❌ отмена"}:
        await state.clear()
        await message.answer(
            locales.t(lang, "cancelled"), reply_markup=keyboards.remove_keyboard()
        )
        return

    cleaned = validate_full_name(message.text)
    if not cleaned:
        await message.answer(locales.t(lang, "invalid_name"))
        return

    await state.update_data(full_name=cleaned)
    await state.set_state(Registration.phone)
    await message.answer(
        locales.t(lang, "ask_phone"),
        reply_markup=keyboards.phone_keyboard(lang),
    )


# ----- 3) Telefon raqam qabul qilish -----

@router.message(StateFilter(Registration.phone), F.contact)
async def on_phone_contact(
    message: Message, state: FSMContext, db: Database
) -> None:
    """Kontakt tugma orqali yuborilgan raqam."""
    lang = await _lang(state, db, message.from_user.id)
    phone = normalize_phone(message.contact.phone_number)
    if not phone:
        await message.answer(locales.t(lang, "invalid_phone"))
        return
    await _save_phone_and_ask_region(message, state, lang, phone)


@router.message(StateFilter(Registration.phone), F.text)
async def on_phone_text(
    message: Message, state: FSMContext, db: Database
) -> None:
    """Qo'lda kiritilgan telefon raqam."""
    lang = await _lang(state, db, message.from_user.id)

    if message.text.strip().lower() in {"/cancel", "❌ bekor qilish", "❌ отмена"}:
        await state.clear()
        await message.answer(
            locales.t(lang, "cancelled"), reply_markup=keyboards.remove_keyboard()
        )
        return

    phone = normalize_phone(message.text)
    if not phone:
        await message.answer(locales.t(lang, "invalid_phone"))
        return
    await _save_phone_and_ask_region(message, state, lang, phone)


async def _save_phone_and_ask_region(
    message: Message, state: FSMContext, lang: str, phone: str
) -> None:
    """Telefonni saqlab, viloyat so'raydi."""
    await state.update_data(phone=phone)
    await state.set_state(Registration.region)

    # 1) Reply klaviaturani olib tashlash — qisqa "✅" xabari bilan
    ack = await message.answer("✅", reply_markup=keyboards.remove_keyboard())
    # Texnik xabarni darhol o'chirib yuboramiz, foydalanuvchini chalg'itmasligi uchun
    try:
        await ack.delete()
    except Exception:
        pass

    # 2) Viloyat so'rovi — inline klaviatura bilan
    await message.answer(
        locales.t(lang, "ask_region"),
        reply_markup=keyboards.regions_keyboard(),
    )


# ----- 4) Viloyat tanlash -----

@router.callback_query(StateFilter(Registration.region), F.data.startswith("region:"))
async def on_region(
    call: CallbackQuery, state: FSMContext, db: Database
) -> None:
    try:
        idx = int(call.data.split(":", 1)[1])
        region = locales.REGIONS[idx]
    except (ValueError, IndexError):
        await call.answer("?", show_alert=False)
        return

    lang = await _lang(state, db, call.from_user.id)
    await state.update_data(region=region)
    await state.set_state(Registration.level)

    await call.message.edit_text(
        locales.t(lang, "ask_level"),
        reply_markup=keyboards.levels_keyboard(lang),
    )
    await call.answer()


# ----- 5) Bosqich tanlash -----

@router.callback_query(StateFilter(Registration.level), F.data.startswith("level:"))
async def on_level(
    call: CallbackQuery, state: FSMContext, db: Database
) -> None:
    level_key = call.data.split(":", 1)[1]
    if level_key not in locales.LEVELS:
        await call.answer("?", show_alert=False)
        return

    lang = await _lang(state, db, call.from_user.id)
    await state.update_data(level_key=level_key, level=locales.level_label(level_key))
    await state.set_state(Registration.direction)

    await call.message.edit_text(
        locales.t(lang, "ask_direction"),
        reply_markup=keyboards.directions_keyboard(level_key, lang),
    )
    await call.answer()


# ----- 6) Yo'nalish tanlash -----

@router.callback_query(StateFilter(Registration.direction), F.data.startswith("dir:"))
async def on_direction(
    call: CallbackQuery, state: FSMContext, db: Database
) -> None:
    try:
        idx = int(call.data.split(":", 1)[1])
        data = await state.get_data()
        level_key = data.get("level_key", "")
        directions = locales.directions_for(level_key)
        direction = directions[idx]
    except (ValueError, IndexError, KeyError):
        await call.answer("?", show_alert=False)
        return

    lang = await _lang(state, db, call.from_user.id)
    await state.update_data(direction=direction)
    await state.set_state(Registration.confirm)

    data = await state.get_data()
    summary = locales.t(
        lang,
        "summary",
        full_name=data["full_name"],
        phone=data["phone"],
        region=data["region"],
        level=data["level"],
        direction=data["direction"],
    )
    await call.message.edit_text(
        summary, reply_markup=keyboards.confirm_keyboard(lang)
    )
    await call.answer()


# ----- Orqaga qaytish -----

@router.callback_query(StateFilter(Registration.level), F.data == "back:region")
async def on_back_to_region(
    call: CallbackQuery, state: FSMContext, db: Database
) -> None:
    """Bosqich ekranidan -> viloyat ekraniga qaytish."""
    lang = await _lang(state, db, call.from_user.id)
    await state.set_state(Registration.region)
    await call.message.edit_text(
        locales.t(lang, "ask_region"),
        reply_markup=keyboards.regions_keyboard(),
    )
    await call.answer()


@router.callback_query(StateFilter(Registration.direction), F.data == "back:level")
async def on_back_to_level(
    call: CallbackQuery, state: FSMContext, db: Database
) -> None:
    """Yo'nalish ekranidan -> bosqich ekraniga qaytish."""
    lang = await _lang(state, db, call.from_user.id)
    await state.set_state(Registration.level)
    await call.message.edit_text(
        locales.t(lang, "ask_level"),
        reply_markup=keyboards.levels_keyboard(lang),
    )
    await call.answer()


# ----- 7) Tasdiqlash / qaytadan -----

@router.callback_query(StateFilter(Registration.confirm), F.data == "confirm:retry")
async def on_retry(call: CallbackQuery, state: FSMContext, db: Database) -> None:
    """Anketani qaytadan to'ldirish."""
    lang = await _lang(state, db, call.from_user.id)
    # Tilni saqlab qolib, qolganini tozalaymiz
    await state.clear()
    await state.update_data(language=lang)
    await state.set_state(Registration.full_name)
    await call.message.edit_text(locales.t(lang, "ask_full_name"))
    await call.answer()


@router.callback_query(StateFilter(Registration.confirm), F.data == "confirm:yes")
async def on_confirm(
    call: CallbackQuery, state: FSMContext, db: Database, bot: Bot
) -> None:
    """Arizani DB'ga saqlab, adminga yuborish."""
    try:
        lang = await _lang(state, db, call.from_user.id)
        data = await state.get_data()

        username = call.from_user.username
        payload = {
            "telegram_id": call.from_user.id,
            "username": username,
            "language": lang,
            "full_name": data["full_name"],
            "phone": data["phone"],
            "region": data["region"],
            "level": data["level"],
            "direction": data["direction"],
        }

        app_id = await db.add_application(payload)

        # Foydalanuvchiga yakuniy xabar
        await call.message.edit_text(
            locales.t(
                lang,
                "finish",
                phone=config.UNIVERSITY_PHONE,
                site=config.UNIVERSITY_SITE,
            )
        )

        # Adminga xabar
        await _notify_admin(bot, app_id, payload)

        await state.clear()
        await call.answer()
    except Exception:
        logger.exception("on_confirm xatosi")
        await call.answer(locales.t("uz", "error_generic"), show_alert=True)


async def _notify_admin(bot: Bot, app_id: int, payload: dict) -> None:
    """Adminga yangi ariza haqida xabar yuborish."""
    try:
        username = payload.get("username")
        admin_text = locales.ADMIN_TEXTS["new_application_admin"].format(
            id=app_id,
            full_name=payload["full_name"],
            phone=payload["phone"],
            region=payload["region"],
            level=payload["level"],
            direction=payload["direction"],
            language="O'zbek" if payload["language"] == "uz" else "Русский",
            telegram_id=payload["telegram_id"],
            username=f"@{username}" if username else "—",
            time=datetime.now().strftime("%d.%m.%Y %H:%M"),
        )
        await bot.send_message(
            chat_id=config.ADMIN_ID,
            text=admin_text,
            reply_markup=keyboards.admin_application_keyboard(
                app_id, payload["telegram_id"]
            ),
        )
        logger.info("Admin xabardor qilindi: ariza #%s", app_id)
    except Exception:
        logger.exception("Adminga xabar yuborishda xato")
