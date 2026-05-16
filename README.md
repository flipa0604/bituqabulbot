# 🎓 BITU Qabul Boti

Buxoro Innovatsion Ta'lim va Tibbiyot Universiteti (BITU) uchun Telegram qabul boti.
Abituriyentlardan anketa ma'lumotlarini yig'adi, SQLite bazasiga saqlaydi va adminga real vaqtda xabar yuboradi.

## ✨ Xususiyatlar

- 🇺🇿🇷🇺 **Ikki tilli interfeys** — O'zbek va Rus
- 📋 **FSM asosida anketa** — har bir qadam alohida holat
- 💾 **SQLite + aiosqlite** — asinxron, portativ baza
- 👨‍💼 **Admin panel** — statistika, ro'yxat, Excel eksport, status boshqaruvi
- 📞 **Telefon validatsiyasi** — `+998 XX XXX XX XX` formatga normallashtirish
- 🔔 **Yangi ariza haqida adminga inline tugmali xabar** (bog'lanish, status o'zgartirish)
- ⏳ **Rate limiting** — 1 daqiqada 30 xabardan ortig'i bloklanadi
- 📝 **Loglar** — konsol + `bot.log` fayli
- 🧯 **Xato boshqaruv** — har bir handler try/except ichida

## 📦 Talablar

- Python **3.10+**
- aiogram **3.13+**
- aiosqlite, python-dotenv, openpyxl

## 🚀 Ishga tushirish

### 1. Loyihani klon qiling va virtual muhit yarating

```bash
cd "bitu qabul bot"
python -m venv .venv
```

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

### 2. Kutubxonalarni o'rnating

```bash
pip install -r requirements.txt
```

### 3. `.env` faylni sozlang

`.env.example` faylni `.env` deb nusxalang va o'z qiymatlaringizni kiriting:

```env
BOT_TOKEN=1234567890:AAH...    # @BotFather'dan olingan token
ADMIN_ID=123456789              # Admin Telegram ID (raqam)
DATABASE_PATH=bitu.db           # Baza fayli (ixtiyoriy)
```

> **ADMIN_ID ni qanday bilish kerak?** Telegram'da [@userinfobot](https://t.me/userinfobot) ga `/start` yuboring.

### 4. Botni ishga tushiring

```bash
python main.py
```

Konsolda quyidagiga o'xshash xabar chiqsa, hammasi tayyor:

```
2026-05-16 14:30:00 | INFO | __main__ | Bot ishga tushdi: @bitu_qabul_bot (id=...)
```

## 🗂 Fayl tuzilishi

```
bitu_bot/
├── .env                    # Maxfiy sozlamalar (commit qilinmaydi)
├── .env.example            # Sozlama namunasi
├── requirements.txt
├── main.py                 # Kirish nuqtasi
├── config.py               # BOT_TOKEN, ADMIN_ID, logging
├── database.py             # SQLite qatlami
├── locales.py              # uz/ru matnlar, viloyat/yo'nalish ro'yxati
├── keyboards.py            # Inline + Reply tugmalar
├── states.py               # FSM holatlari
├── middlewares.py          # Rate limiting
├── handlers/
│   ├── start.py            # /start, til, /language, /cancel
│   ├── registration.py     # Anketa to'ldirish FSM
│   └── admin.py            # /admin, /stats, /list, /export
└── utils/
    └── validators.py       # F.I.O va telefon validatsiya
```

## 👤 Foydalanuvchi tajribasi

1. `/start` — til tanlash (🇺🇿 / 🇷🇺)
2. Boshlash tugmasi
3. F.I.O kiritish
4. Telefon raqam (kontakt tugma orqali yoki qo'lda)
5. Viloyat tanlash
6. Bosqich tanlash (Bakalavr / Magistratura / Klinik ordinatura)
7. Yo'nalish tanlash (bosqichga bog'liq)
8. Tasdiqlash — barcha ma'lumot ko'rsatiladi
9. Yakuniy minnatdorlik xabari + adminga avtomatik xabar

## 👨‍💼 Admin buyruqlari

Faqat `.env` dagi `ADMIN_ID` uchun ishlaydi:

| Buyruq | Vazifa |
|---|---|
| `/admin` | Panel — buyruqlar ro'yxati |
| `/stats` | Umumiy statistika (jami, bugungi, bosqich, top yo'nalishlar) |
| `/list` | Oxirgi 10 ta arizani ko'rsatadi |
| `/export` | Barcha arizalarni `.xlsx` faylga eksport qiladi |

Har bir yangi ariza xabari ostida 4 ta tugma bo'ladi:
- **📞 Bog'lanish** — to'g'ridan-to'g'ri foydalanuvchiga yozish
- **✅ Bog'landim** / **🎓 Qabul qilindi** / **❌ Rad etildi** — status o'zgartirish

## 🛠 Boshqa foydalanuvchi buyruqlari

| Buyruq | Vazifa |
|---|---|
| `/start` | Botni qayta boshlash |
| `/language` | Tilni o'zgartirish |
| `/cancel` | Joriy anketani bekor qilish |

## 🗄 Ma'lumotlar bazasi

Bot ilk ishga tushirilganda `bitu.db` (yoki `.env` dagi `DATABASE_PATH`) avtomatik yaratiladi. Jadvallar:

- `applications` — barcha arizalar (id, telegram_id, f.i.o, telefon, viloyat, bosqich, yo'nalish, status, vaqt)
- `users` — foydalanuvchi tili va so'nggi faollik vaqti

## 📄 Loglar

Barcha hodisalar (yangi ariza, xato, admin harakatlari) `bot.log` fayliga yoziladi.

## 🐞 Tez-tez uchraydigan muammolar

**`RuntimeError: BOT_TOKEN topilmadi`** — `.env` fayl mavjud emas yoki ichida `BOT_TOKEN` yo'q.

**Adminga xabar bormayapti** — `ADMIN_ID` noto'g'ri yoki admin botni bloklab qo'ygan. Admin avval botga `/start` yuborgan bo'lishi kerak.

**Excel eksport ishlamayapti** — `openpyxl` o'rnatilmagan: `pip install openpyxl`.

## 📜 Litsenziya

Loyiha ichki foydalanish uchun.
