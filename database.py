"""
SQLite bilan ishlash uchun asinxron qatlam.
aiosqlite kutubxonasi orqali.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Optional

import aiosqlite

logger = logging.getLogger(__name__)


# Jadval sxemalari
SCHEMA_APPLICATIONS = """
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL,
    username TEXT,
    language TEXT NOT NULL,
    full_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    region TEXT NOT NULL,
    level TEXT NOT NULL,
    direction TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'new'
)
"""

SCHEMA_USERS = """
CREATE TABLE IF NOT EXISTS users (
    telegram_id INTEGER PRIMARY KEY,
    language TEXT,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

INDEX_APPLICATIONS_TG = (
    "CREATE INDEX IF NOT EXISTS idx_applications_tg "
    "ON applications(telegram_id)"
)
INDEX_APPLICATIONS_CREATED = (
    "CREATE INDEX IF NOT EXISTS idx_applications_created "
    "ON applications(created_at)"
)


class Database:
    """SQLite ulanishini boshqaruvchi sinf."""

    def __init__(self, path: str) -> None:
        self.path = path
        self._conn: Optional[aiosqlite.Connection] = None

    async def init(self) -> None:
        """Ulanishni ochib, jadvallarni yaratadi."""
        self._conn = await aiosqlite.connect(self.path)
        self._conn.row_factory = aiosqlite.Row
        await self._conn.execute("PRAGMA foreign_keys = ON")
        await self._conn.execute(SCHEMA_APPLICATIONS)
        await self._conn.execute(SCHEMA_USERS)
        await self._conn.execute(INDEX_APPLICATIONS_TG)
        await self._conn.execute(INDEX_APPLICATIONS_CREATED)
        await self._conn.commit()
        logger.info("Database tayyor: %s", self.path)

    async def close(self) -> None:
        if self._conn is not None:
            await self._conn.close()
            self._conn = None

    @property
    def conn(self) -> aiosqlite.Connection:
        if self._conn is None:
            raise RuntimeError("Database hali init() qilinmagan")
        return self._conn

    # ----- users -----

    async def upsert_user(self, telegram_id: int, language: str) -> None:
        """Foydalanuvchini yangilaydi yoki yangi qo'shadi."""
        await self.conn.execute(
            """
            INSERT INTO users (telegram_id, language, last_active)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(telegram_id) DO UPDATE SET
                language = excluded.language,
                last_active = CURRENT_TIMESTAMP
            """,
            (telegram_id, language),
        )
        await self.conn.commit()

    async def get_user_language(self, telegram_id: int) -> Optional[str]:
        async with self.conn.execute(
            "SELECT language FROM users WHERE telegram_id = ?",
            (telegram_id,),
        ) as cur:
            row = await cur.fetchone()
            return row["language"] if row else None

    # ----- applications -----

    async def has_application(self, telegram_id: int) -> bool:
        """Foydalanuvchi allaqachon ariza yuborganmi?"""
        async with self.conn.execute(
            "SELECT 1 FROM applications WHERE telegram_id = ? LIMIT 1",
            (telegram_id,),
        ) as cur:
            return await cur.fetchone() is not None

    async def add_application(self, data: dict[str, Any]) -> int:
        """Yangi ariza qo'shadi, ID qaytaradi."""
        cur = await self.conn.execute(
            """
            INSERT INTO applications
                (telegram_id, username, language, full_name,
                 phone, region, level, direction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["telegram_id"],
                data.get("username"),
                data["language"],
                data["full_name"],
                data["phone"],
                data["region"],
                data["level"],
                data["direction"],
            ),
        )
        await self.conn.commit()
        app_id = cur.lastrowid or 0
        logger.info("Yangi ariza #%s saqlandi (tg_id=%s)", app_id, data["telegram_id"])
        return app_id

    async def update_status(self, app_id: int, status: str) -> None:
        await self.conn.execute(
            "UPDATE applications SET status = ? WHERE id = ?",
            (status, app_id),
        )
        await self.conn.commit()

    async def get_application(self, app_id: int) -> Optional[aiosqlite.Row]:
        async with self.conn.execute(
            "SELECT * FROM applications WHERE id = ?", (app_id,)
        ) as cur:
            return await cur.fetchone()

    async def get_latest_applications(
        self, limit: int = 10
    ) -> list[aiosqlite.Row]:
        async with self.conn.execute(
            "SELECT * FROM applications ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ) as cur:
            return await cur.fetchall()

    async def get_all_applications(self) -> list[aiosqlite.Row]:
        async with self.conn.execute(
            "SELECT * FROM applications ORDER BY created_at DESC"
        ) as cur:
            return await cur.fetchall()

    # ----- statistika -----

    async def get_stats(self) -> dict[str, Any]:
        """Umumiy statistikani qaytaradi."""
        today = datetime.now().strftime("%Y-%m-%d")

        async with self.conn.execute(
            "SELECT COUNT(*) AS c FROM applications"
        ) as cur:
            total = (await cur.fetchone())["c"]

        async with self.conn.execute(
            "SELECT COUNT(*) AS c FROM applications WHERE DATE(created_at) = ?",
            (today,),
        ) as cur:
            today_count = (await cur.fetchone())["c"]

        async with self.conn.execute(
            "SELECT level, COUNT(*) AS c FROM applications GROUP BY level"
        ) as cur:
            by_level = {row["level"]: row["c"] for row in await cur.fetchall()}

        async with self.conn.execute(
            """
            SELECT direction, COUNT(*) AS c
            FROM applications
            GROUP BY direction
            ORDER BY c DESC
            LIMIT 5
            """
        ) as cur:
            top_directions = [
                (row["direction"], row["c"]) for row in await cur.fetchall()
            ]

        return {
            "total": total,
            "today": today_count,
            "by_level": by_level,
            "top_directions": top_directions,
        }
