"""
Admin handler'lari — /admin, /stats, /list, /export, status o'zgartirish.
"""
from __future__ import annotations

import io
import logging
from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from openpyxl import Workbook

import config
import locales
from database import Database

logger = logging.getLogger(__name__)
router = Router(name="admin")


# Faqat adminlar uchun ishlaydigan filtr (bir nechta admin qo'llab-quvvatlanadi)
def _is_admin(user_id: int) -> bool:
    return user_id in config.ADMIN_IDS


@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        await message.answer(locales.t("uz", "admin_only"))
        return
    await message.answer(locales.ADMIN_TEXTS["panel"])


@router.message(Command("stats"))
async def cmd_stats(message: Message, db: Database) -> None:
    if not _is_admin(message.from_user.id):
        await message.answer(locales.t("uz", "admin_only"))
        return

    stats = await db.get_stats()
    by_level = (
        "\n".join(f"  • {k}: <b>{v}</b>" for k, v in stats["by_level"].items())
        or "  —"
    )
    top = (
        "\n".join(
            f"  {i + 1}. {name} — <b>{count}</b>"
            for i, (name, count) in enumerate(stats["top_directions"])
        )
        or "  —"
    )
    await message.answer(
        locales.ADMIN_TEXTS["stats"].format(
            total=stats["total"],
            today=stats["today"],
            by_level=by_level,
            top=top,
        )
    )


@router.message(Command("list"))
async def cmd_list(message: Message, db: Database) -> None:
    if not _is_admin(message.from_user.id):
        await message.answer(locales.t("uz", "admin_only"))
        return

    rows = await db.get_latest_applications(limit=10)
    if not rows:
        await message.answer(locales.ADMIN_TEXTS["no_applications"])
        return

    for row in rows:
        # created_at — DB'da TEXT/TIMESTAMP. Formatlash uchun harakat.
        created = row["created_at"]
        try:
            dt = datetime.fromisoformat(str(created))
            created_str = dt.strftime("%d.%m.%Y %H:%M")
        except (ValueError, TypeError):
            created_str = str(created)

        text = locales.ADMIN_TEXTS["list_item"].format(
            id=row["id"],
            full_name=row["full_name"],
            phone=row["phone"],
            region=row["region"],
            level=row["level"],
            direction=row["direction"],
            created_at=created_str,
            status=row["status"],
        )
        await message.answer(text)


@router.message(Command("export"))
async def cmd_export(message: Message, db: Database) -> None:
    if not _is_admin(message.from_user.id):
        await message.answer(locales.t("uz", "admin_only"))
        return

    rows = await db.get_all_applications()
    if not rows:
        await message.answer(locales.ADMIN_TEXTS["export_empty"])
        return

    # Excel fayl yaratish
    wb = Workbook()
    ws = wb.active
    ws.title = "Arizalar"
    ws.append([
        "ID",
        "Telegram ID",
        "Username",
        "Til",
        "F.I.O",
        "Telefon",
        "Viloyat",
        "Bosqich",
        "Yo'nalish",
        "Status",
        "Yaratilgan vaqt",
    ])
    for row in rows:
        ws.append([
            row["id"],
            row["telegram_id"],
            row["username"] or "",
            row["language"],
            row["full_name"],
            row["phone"],
            row["region"],
            row["level"],
            row["direction"],
            row["status"],
            str(row["created_at"]),
        ])

    # Ustun kengligini biroz sozlash
    widths = [6, 14, 18, 6, 24, 18, 20, 22, 30, 12, 20]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = w

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)

    filename = f"arizalar_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    document = BufferedInputFile(buf.getvalue(), filename=filename)
    await message.answer_document(
        document=document,
        caption=locales.ADMIN_TEXTS["export_caption"].format(count=len(rows)),
    )
    logger.info("Admin eksport oldi: %s ta ariza", len(rows))


# ----- Status o'zgartirish (inline tugmalar) -----

_STATUS_LABELS = {
    "contacted": "Bog'lanildi",
    "accepted": "Qabul qilindi",
    "rejected": "Rad etildi",
}


@router.callback_query(F.data.startswith("admin_status:"))
async def on_admin_status(call: CallbackQuery, db: Database) -> None:
    if not _is_admin(call.from_user.id):
        await call.answer(locales.t("uz", "admin_only"), show_alert=True)
        return

    try:
        _, new_status, app_id_s = call.data.split(":")
        app_id = int(app_id_s)
    except (ValueError, IndexError):
        await call.answer("?", show_alert=False)
        return

    if new_status not in _STATUS_LABELS:
        await call.answer("?", show_alert=False)
        return

    await db.update_status(app_id, new_status)
    label = _STATUS_LABELS[new_status]
    logger.info("Admin status: ariza #%s -> %s", app_id, new_status)

    # Asl xabarga status qo'shimchasini biriktiramiz
    try:
        await call.message.edit_text(
            (call.message.html_text or "")
            + f"\n\n<b>📌 Status:</b> {label}",
            reply_markup=None,
        )
    except Exception:
        # edit imkoni bo'lmasa — yangi xabar
        await call.message.answer(
            locales.ADMIN_TEXTS["status_updated"].format(status=label)
        )
    await call.answer(
        locales.ADMIN_TEXTS["status_updated"].format(status=label).replace("<b>", "").replace("</b>", "")
    )
