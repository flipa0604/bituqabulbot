"""
O'zbek va Rus tilidagi matnlar.
Foydalanish: t(lang, "key", **format_args)
"""
from __future__ import annotations

# Viloyatlar — kalit ichki saqlash uchun, qiymat — chiqarish uchun.
# Ikkala tilda bir xil yoziladi (rus tilida ham mahalliy nomlar).
REGIONS = [
    "Toshkent shahri",
    "Toshkent viloyati",
    "Andijon",
    "Buxoro",
    "Farg'ona",
    "Jizzax",
    "Xorazm",
    "Namangan",
    "Navoiy",
    "Qashqadaryo",
    "Qoraqalpog'iston",
    "Samarqand",
    "Sirdaryo",
    "Surxondaryo",
]

# Bosqichlar
LEVELS = {
    "bachelor": "🎓 Bakalavr",
    "master": "📚 Magistratura",
    "ordinator": "🩺 Klinik ordinatura",
}

# Yo'nalishlar — bosqich kalitiga bog'liq
DIRECTIONS: dict[str, list[str]] = {
    "bachelor": [
        "Davolash ishi",
        "Stomatologiya",
        "Iqtisodiyot",
        "Psixologiya",
        "Boshlang'ich ta'lim",
        "Filologiya va tillarni o'qitish",
    ],
    "master": [
        "O'zbek tili va adabiyoti",
        "Terapevtik stomatologiya",
        "Neyroxirurgiya",
        "Akusherlik va Ginekologiya",
        "Travmatologiya va ortopediya",
        "Ortopedik stomatologiya",
        "Bolalar jarrohlik stomatologiyasi",
        "Bolalar terapevtik stomatologiyasi",
        "Yuz-jag' xirurgiyasi",
    ],
    "ordinator": [
        "Pediatriya",
        "Bolalar stomatologiyasi",
        "Ortopedik stomatologiya",
        "Diyetologiya",
        "Terapevtik stomatologiya",
        "Neonatologiya",
        "Radiologiya",
        "Endokrinologiya",
        "Yuqumli kasalliklar",
        "Laboratoriya ishi",
        "Otorinolaringologiya",
        "Dermatovenerologiya",
        "Kardiologiya",
        "Bolalar nevrologiyasi",
        "Bolalar jarrohligi",
        "Anesteziologiya-ortopediya",
        "Travmatologiya-ortopediya",
        "Onkologiya",
        "Xirurgiya",
    ],
}


# Matnlar lug'ati. Har bir kalit — uz va ru.
TEXTS: dict[str, dict[str, str]] = {
    "welcome": {
        "uz": (
            "🎓 <b>Assalomu alaykum!</b>\n\n"
            "Buxoro Innovatsion Ta'lim va Tibbiyot Universiteti\n"
            "qabul botiga xush kelibsiz.\n\n"
            "Iltimos, tilni tanlang / Пожалуйста, выберите язык:"
        ),
        "ru": (
            "🎓 <b>Assalomu alaykum!</b>\n\n"
            "Buxoro Innovatsion Ta'lim va Tibbiyot Universiteti\n"
            "qabul botiga xush kelibsiz.\n\n"
            "Iltimos, tilni tanlang / Пожалуйста, выберите язык:"
        ),
    },
    "intro": {
        "uz": (
            "✨ <b>Bizning universitetda o'qish — kelajakka qo'yilgan eng to'g'ri qadam!</b>\n\n"
            "Qabulga yozilish uchun quyidagi qisqa anketani to'ldiring.\n"
            "Bu bor-yo'g'i 1-2 daqiqa vaqtingizni oladi."
        ),
        "ru": (
            "✨ <b>Учёба в нашем университете — самый верный шаг в будущее!</b>\n\n"
            "Чтобы подать заявку, заполните короткую анкету.\n"
            "Это займёт всего 1–2 минуты."
        ),
    },
    "btn_start": {"uz": "🚀 Boshlash", "ru": "🚀 Начать"},
    "btn_change_lang": {"uz": "🔙 Tilni o'zgartirish", "ru": "🔙 Сменить язык"},
    "btn_send_contact": {"uz": "📲 Raqamni yuborish", "ru": "📲 Отправить номер"},
    "btn_confirm": {"uz": "✅ Tasdiqlash", "ru": "✅ Подтвердить"},
    "btn_retry": {"uz": "🔄 Qaytadan to'ldirish", "ru": "🔄 Заполнить заново"},
    "ask_full_name": {
        "uz": "👤 Iltimos, ism va familiyangizni kiriting:\n\nMasalan: <i>Aliyev Akbar</i>",
        "ru": "👤 Пожалуйста, введите имя и фамилию:\n\nНапример: <i>Алиев Акбар</i>",
    },
    "ask_phone": {
        "uz": "📱 Telefon raqamingizni kiriting yoki pastdagi tugma orqali yuboring:",
        "ru": "📱 Введите ваш номер телефона или отправьте его кнопкой ниже:",
    },
    "ask_region": {
        "uz": "📍 Qaysi viloyatdansiz? Tanlang:",
        "ru": "📍 Из какой области вы? Выберите:",
    },
    "ask_level": {
        "uz": "🎓 Qaysi bosqichga hujjat topshirmoqchisiz?",
        "ru": "🎓 На какой уровень вы хотите подать документы?",
    },
    "ask_direction": {
        "uz": "📖 Yo'nalishni tanlang:",
        "ru": "📖 Выберите направление:",
    },
    "summary": {
        "uz": (
            "📋 <b>Ma'lumotlaringizni tekshiring:</b>\n\n"
            "👤 <b>F.I.O:</b> {full_name}\n"
            "📱 <b>Telefon:</b> {phone}\n"
            "📍 <b>Viloyat:</b> {region}\n"
            "🎓 <b>Bosqich:</b> {level}\n"
            "📖 <b>Yo'nalish:</b> {direction}\n\n"
            "Hammasi to'g'rimi?"
        ),
        "ru": (
            "📋 <b>Проверьте ваши данные:</b>\n\n"
            "👤 <b>Ф.И.О:</b> {full_name}\n"
            "📱 <b>Телефон:</b> {phone}\n"
            "📍 <b>Область:</b> {region}\n"
            "🎓 <b>Уровень:</b> {level}\n"
            "📖 <b>Направление:</b> {direction}\n\n"
            "Всё верно?"
        ),
    },
    "finish": {
        "uz": (
            "🎉 <b>Tabriklaymiz! Arizangiz qabul qilindi.</b>\n\n"
            "Tez orada qabul bo'limi xodimlari siz bilan\n"
            "bog'lanishadi. BITU oilasiga xush kelibsiz!\n\n"
            "📞 Murojaat: {phone}\n"
            "🌐 Sayt: {site}"
        ),
        "ru": (
            "🎉 <b>Поздравляем! Ваша заявка принята.</b>\n\n"
            "Сотрудники приёмной комиссии скоро\n"
            "свяжутся с вами. Добро пожаловать в семью BITU!\n\n"
            "📞 Контакт: {phone}\n"
            "🌐 Сайт: {site}"
        ),
    },
    "already_applied": {
        "uz": (
            "ℹ️ Siz allaqachon ariza yuborgansiz.\n\n"
            "Yangi ariza yuborishni xohlaysizmi?"
        ),
        "ru": (
            "ℹ️ Вы уже отправляли заявку.\n\n"
            "Хотите отправить новую?"
        ),
    },
    "btn_new_application": {
        "uz": "✏️ Yangi ariza",
        "ru": "✏️ Новая заявка",
    },
    "btn_cancel": {"uz": "❌ Bekor qilish", "ru": "❌ Отмена"},
    "cancelled": {
        "uz": "❌ Anketa bekor qilindi. Qaytadan boshlash uchun /start bosing.",
        "ru": "❌ Анкета отменена. Нажмите /start чтобы начать заново.",
    },
    "invalid_name": {
        "uz": (
            "⚠️ Iltimos, ism va familiyangizni to'g'ri kiriting.\n"
            "Kamida 2 ta so'z, faqat harflardan iborat bo'lsin."
        ),
        "ru": (
            "⚠️ Пожалуйста, корректно введите имя и фамилию.\n"
            "Минимум 2 слова, только буквы."
        ),
    },
    "invalid_phone": {
        "uz": (
            "⚠️ Telefon raqam noto'g'ri.\n"
            "Format: <code>+998 90 123 45 67</code>"
        ),
        "ru": (
            "⚠️ Неверный номер телефона.\n"
            "Формат: <code>+998 90 123 45 67</code>"
        ),
    },
    "error_generic": {
        "uz": "😔 Xatolik yuz berdi. Iltimos, /start orqali qaytadan boshlang.",
        "ru": "😔 Произошла ошибка. Пожалуйста, начните заново через /start.",
    },
    "rate_limited": {
        "uz": "⏳ Juda ko'p so'rov. Bir oz kuting.",
        "ru": "⏳ Слишком много запросов. Подождите немного.",
    },
    "lang_changed": {
        "uz": "✅ Til o'zgartirildi. /start bosing.",
        "ru": "✅ Язык изменён. Нажмите /start.",
    },
    "level_names": {
        # forward fill — bosqichlar nomi tarjima qilinmaydi, lekin
        # kerak bo'lsa shu yerdan kengaytirish mumkin.
        "uz": "",
        "ru": "",
    },
    "admin_only": {
        "uz": "🚫 Bu buyruq faqat admin uchun.",
        "ru": "🚫 Эта команда только для администратора.",
    },
}


# Admin paneliga oid matnlar (faqat o'zbek tilida — admin uchun)
ADMIN_TEXTS = {
    "panel": (
        "👨‍💼 <b>Admin panel</b>\n\n"
        "Buyruqlar:\n"
        "/stats — statistika\n"
        "/list — oxirgi 10 ta ariza\n"
        "/export — barcha arizalarni Excel'ga eksport"
    ),
    "stats": (
        "📊 <b>Statistika</b>\n\n"
        "Jami arizalar: <b>{total}</b>\n"
        "Bugungi arizalar: <b>{today}</b>\n\n"
        "<b>Bosqichlar bo'yicha:</b>\n{by_level}\n\n"
        "<b>Eng ommabop yo'nalishlar:</b>\n{top}"
    ),
    "no_applications": "📭 Hozircha arizalar yo'q.",
    "list_item": (
        "<b>#{id}</b> — {full_name}\n"
        "📱 {phone} | 📍 {region}\n"
        "🎓 {level} → {direction}\n"
        "🕐 {created_at} | Status: <b>{status}</b>"
    ),
    "new_application_admin": (
        "🆕 <b>YANGI ARIZA #{id}</b>\n\n"
        "👤 <b>F.I.O:</b> {full_name}\n"
        "📱 <b>Telefon:</b> {phone}\n"
        "📍 <b>Viloyat:</b> {region}\n"
        "🎓 <b>Bosqich:</b> {level}\n"
        "📖 <b>Yo'nalish:</b> {direction}\n"
        "🌐 <b>Til:</b> {language}\n"
        "🆔 <b>Telegram ID:</b> <code>{telegram_id}</code>\n"
        "👤 <b>Username:</b> {username}\n"
        "🕐 <b>Vaqt:</b> {time}"
    ),
    "btn_contact": "📞 Bog'lanish",
    "btn_status_contacted": "✅ Bog'landim",
    "btn_status_accepted": "🎓 Qabul qilindi",
    "btn_status_rejected": "❌ Rad etildi",
    "status_updated": "✅ Status yangilandi: <b>{status}</b>",
    "export_caption": "📊 Barcha arizalar ({count} ta)",
    "export_empty": "📭 Eksport qilish uchun ariza yo'q.",
}


def t(lang: str, key: str, **kwargs) -> str:
    """Tilga mos matnni qaytaradi.

    Agar kalit topilmasa yoki til noma'lum bo'lsa, kalitning o'zi qaytadi.
    """
    if lang not in ("uz", "ru"):
        lang = "uz"
    entry = TEXTS.get(key)
    if not entry:
        return key
    text = entry.get(lang) or entry.get("uz") or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text


def level_label(level_key: str) -> str:
    """Bosqich kaliti -> ko'rinadigan nomi."""
    return LEVELS.get(level_key, level_key)


def directions_for(level_key: str) -> list[str]:
    """Bosqichga mos yo'nalishlar ro'yxati."""
    return DIRECTIONS.get(level_key, [])
