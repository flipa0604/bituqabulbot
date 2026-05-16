"""
FSM holatlari — anketa to'ldirish jarayoni.
"""
from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    """Anketa to'ldirish bosqichlari."""

    full_name = State()       # ism familiya kiritish
    phone = State()           # telefon raqam
    region = State()          # viloyat tanlash
    level = State()           # bosqich tanlash
    direction = State()       # yo'nalish tanlash
    confirm = State()         # tasdiqlash
