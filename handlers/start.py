"""
/start, til tanlash, /language, /cancel.
"""
from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import keyboards
import locales
from database import Database
from states import Registration

logger = logging.getLogger(__name__)
router = Router(name="start")


async def _get_lang(db: Database, telegram_id: int) -> str:
    """DB'dan til o'qiydi, topilmasa 'uz' qaytaradi."""
    return await db.get_user_language(telegram_id) or "uz"


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, db: Database) -> None:
    """/start — til tanlash ekrani."""
    await state.clear()
    try:
        # Agar foydalanuvchida ariza bor bo'lsa — xabar berish
        if await db.has_application(message.from_user.id):
            lang = await _get_lang(db, message.from_user.id)
            await message.answer(
                locales.t(lang, "already_applied"),
                reply_markup=keyboards.already_applied_keyboard(lang),
            )
            return

        await message.answer(
            locales.t("uz", "welcome"),
            reply_markup=keyboards.lang_keyboard(),
        )
    except Exception:
        logger.exception("cmd_start xatosi")
        await message.answer(locales.t("uz", "error_generic"))


@router.callback_query(F.data.startswith("lang:"))
async def on_language_chosen(
    call: CallbackQuery, state: FSMContext, db: Database
) -> None:
    """Til tanlangan — welcome xabari saqlanadi, intro yangi xabar bilan keladi."""
    try:
        lang = call.data.split(":", 1)[1]
        if lang not in ("uz", "ru"):
            lang = "uz"
        await db.upsert_user(call.from_user.id, lang)
        await state.update_data(language=lang)

        # Welcome xabarini saqlab qolamiz, faqat til tugmalarini olib tashlaymiz.
        try:
            await call.message.edit_reply_markup(reply_markup=None)
        except Exception:
            pass

        # Intro yangi xabar sifatida yuboriladi
        await call.message.answer(
            locales.t(lang, "intro"),
            reply_markup=keyboards.start_keyboard(lang),
        )
        await call.answer()
    except Exception:
        logger.exception("on_language_chosen xatosi")
        await call.answer(locales.t("uz", "error_generic"), show_alert=True)


@router.callback_query(F.data == "change_lang")
async def on_change_lang(call: CallbackQuery, state: FSMContext) -> None:
    """Tilni qaytadan tanlash — intro xabari welcome bilan almashtiriladi."""
    await state.clear()
    await call.message.edit_text(
        locales.t("uz", "welcome"),
        reply_markup=keyboards.lang_keyboard(),
    )
    await call.answer()


@router.message(Command("language"))
async def cmd_language(message: Message, state: FSMContext) -> None:
    """/language — tilni o'zgartirish istalgan paytda."""
    await state.clear()
    await message.answer(
        locales.t("uz", "welcome"),
        reply_markup=keyboards.lang_keyboard(),
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext, db: Database) -> None:
    """/cancel — anketani bekor qilish."""
    lang = await _get_lang(db, message.from_user.id)
    await state.clear()
    await message.answer(
        locales.t(lang, "cancelled"),
        reply_markup=keyboards.remove_keyboard(),
    )


@router.callback_query(F.data == "new_application")
async def on_new_application(
    call: CallbackQuery, state: FSMContext, db: Database
) -> None:
    """Allaqachon ariza bor — yangi anketani boshlash."""
    lang = await _get_lang(db, call.from_user.id)
    await state.clear()
    await state.update_data(language=lang)

    await call.message.edit_text(
        locales.t(lang, "intro"),
        reply_markup=keyboards.start_keyboard(lang),
    )
    await call.answer()
