"""
Middleware'lar — rate limiting.
"""
from __future__ import annotations

import logging
import time
from collections import defaultdict, deque
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

import locales

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseMiddleware):
    """Foydalanuvchi har soniyada juda ko'p so'rov yubormasligini ta'minlaydi.

    Sliding window algoritmi: deque ichida oxirgi N soniyadagi so'rov vaqtlari.
    """

    def __init__(self, max_messages: int = 30, window_seconds: int = 60) -> None:
        self.max_messages = max_messages
        self.window_seconds = window_seconds
        self._history: dict[int, deque[float]] = defaultdict(deque)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        now = time.monotonic()
        bucket = self._history[user.id]

        # Eski yozuvlarni o'chirish
        cutoff = now - self.window_seconds
        while bucket and bucket[0] < cutoff:
            bucket.popleft()

        if len(bucket) >= self.max_messages:
            logger.warning(
                "Rate limit triggered: user=%s, count=%s",
                user.id,
                len(bucket),
            )
            # Foydalanuvchi tilini bilmasak, default uz
            lang = "uz"
            try:
                if isinstance(event, Message):
                    await event.answer(locales.t(lang, "rate_limited"))
                elif isinstance(event, CallbackQuery):
                    await event.answer(
                        locales.t(lang, "rate_limited"), show_alert=True
                    )
            except Exception:
                pass
            return None

        bucket.append(now)
        return await handler(event, data)
