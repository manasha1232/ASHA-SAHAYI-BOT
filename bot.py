from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)
from deep_translator import GoogleTranslator
import sqlite3
from datetime import datetime

# =========================
# 🔐 CONFIG
# =========================
BOT_TOKEN = "8561878088:xxxxxxxxxxxxxxxxxxxxxxxx"
MANAGER_CHAT_ID = 123456789  # replace with real Telegram chat ID

DB_NAME = "asha_sahayi.db"

# =========================
# 🗄️ DATABASE
# =========================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient_visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT,
            symptoms TEXT,
            issue TEXT,
            duration_days INTEGER,
            advice TEXT,
            responded INTEGER DEFAULT 0,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_visit(chat_id, symptoms, issue, duration_days, advice):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patient_visits
        (chat_id, symptoms, issue, duration_days, advice, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        chat_id,
        symptoms,
        issue,
        duration_days,
        advice,
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def mark_responded(chat_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE patient_visits
        SET responded = 1
        WHERE chat_id = ?
        ORDER BY id DESC LIMIT 1
    """, (chat_id,))
    conn.commit()
    conn.close()

def last_response_status(chat_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT responded FROM patient_visits
        WHERE chat_id = ?
        ORDER BY id DESC LIMIT 1
    """, (chat_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

# =========================
# 🌐 LANGUAGE
# =========================
def normalize_input(text):
    try:
        return GoogleTranslator(source="auto", target="ta").translate(text)
    except:
        return text

# =========================
# ⏱️ DURATION
# =========================
def extract_duration(text):
    text = text.lower()
    for i in range(1, 15):
        if f"{i} naal" in text or f"{i} நாள்" in text:
            return i
        if f"{i} day" in text or f"{i} days" in text:
            return i
    if "week" in text or "வாரம்" in text:
        return 7
    if "hour" in text or "hrs" in text or "மணி" in text:
        return 0
    return None

# =========================
# 🧠 MEDICAL LOGIC
# =========================
def local_medical_ai(text, duration_days):
    text = text.lower()

    emergency_words = [
        "blood vomit", "vomiting blood", "blood in vomit",
        "blood in stool", "bloody stool",
        "இரத்த வாந்தி", "ரத்த வாந்தி", "இரத்தம்", "ரத்தம்"
    ]

    if any(w in text for w in emergency_words):
        return {
            "reply": (
                "🚨 **அவசர நிலை** 🚨\n\n"
                "வாந்தி அல்லது மலத்தில் இரத்தம் காணப்படுவது மிகவும் ஆபத்தானது.\n\n"
                "👉 **உடனடியாக அரசு மருத்துவமனைக்கு அனுப்பவும்.**\n"
                "👉 வீட்டுச் சிகிச்சைகள் செய்ய வேண்டாம்."
            ),
            "issue": "emergency",
            "advice": "hospital"
        }

    fever_words = ["fever", "காய்ச்சல்"]
    cough_words = ["cough", "இருமல்"]
    stomach_words = ["vomit", "vomiting", "loose motion", "diarrhea", "வயிறு"]
    weakness_words = ["weak", "tired", "fatigue", "சோர்வு"]

    scores = {
        "fever": sum(w in text for w in fever_words),
        "cough": sum(w in text for w in cough_words),
        "stomach": sum(w in text for w in stomach_words),
        "weakness": sum(w in text for w in weakness_words),
    }

    issue = max(scores, key=scores.get)

    if issue == "fever" and scores["fever"] > 0:
        if duration_days is not None and duration_days >= 3:
            return {
                "reply": (
                    "⚠️ 3 நாட்களுக்கு மேல் காய்ச்சல் நீடிக்கிறது.\n"
                    "👉 அரசு மருத்துவமனைக்கு அனுப்பவும்."
                ),
                "issue": "fever",
                "advice": "hospital"
            }
        return {
            "reply": (
                "காய்ச்சல் லேசான தொற்று காரணமாக இருக்கலாம்.\n"
                "✔ ஓய்வு\n✔ வெதுவெதுப்பான நீர்\n"
                "2–3 நாட்கள் நீடித்தால் மருத்துவமனைக்கு அனுப்பவும்."
            ),
            "issue": "fever",
            "advice": "home"
        }

    if issue == "cough" and scores["cough"] > 0:
        return {
            "reply": (
                "இருமல் சளி காரணமாக இருக்கலாம்.\n"
                "✔ ஆவி பிடித்தல்\n✔ வெதுவெதுப்பான நீர்\n"
                "மூச்சுத் திணறல் இருந்தால் மருத்துவமனைக்கு அனுப்பவும்."
            ),
            "issue": "cough",
            "advice": "home"
        }

    if issue == "stomach" and scores["stomach"] > 0:
        return {
            "reply": (
                "வயிற்றுப் பிரச்சனை உணவு காரணமாக இருக்கலாம்.\n"
                "✔ சிறு சிறு அளவில் நீர்\n"
                "நிலை மோசமானால் மருத்துவமனைக்கு அனுப்பவும்."
            ),
            "issue": "stomach",
            "advice": "home"
        }

    if issue == "weakness" and scores["weakness"] > 0:
        return {
            "reply": (
                "உடல் சோர்வு ஓய்வு இல்லாமை காரணமாக இருக்கலாம்.\n"
                "✔ ஓய்வு\n✔ சத்தான உணவு\n"
                "நீடித்தால் மருத்துவமனைக்கு அனுப்பவும்."
            ),
            "issue": "weakness",
            "advice": "home"
        }

    return {
        "reply": (
            "அறிகுறிகள் தெளிவாக இல்லை.\n"
            "✔ ஓய்வு\n"
            "சந்தேகம் இருந்தால் மருத்துவமனைக்கு அனுப்பவும்."
        ),
        "issue": "unknown",
        "advice": "monitor"
    }

# =========================
# 🚨 MANAGER ALERTS
# =========================
async def notify_manager(context, visit):
    msg = (
        "🚨 **EMERGENCY ALERT – ASHA Sahayi** 🚨\n\n"
        f"ASHA Chat ID: {visit['chat_id']}\n"
        f"Symptoms: {visit['symptoms']}\n"
        f"Duration: {visit['duration']} days\n\n"
        "⚠️ Patient advised hospital.\n"
        "❗ No confirmation yet."
    )
    await context.bot.send_message(
        chat_id=MANAGER_CHAT_ID,
        text=msg,
        parse_mode="Markdown"
    )

async def escalate_if_no_response(context):
    data = context.job.data
    status = last_response_status(data["chat_id"])
    if status == 0:
        await notify_manager(context, data)

# =========================
# 👋 /start
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🙏 **வணக்கம்! நான் ASHA Sahayi**\n\n"
        "👉 நோயாளியின் அறிகுறிகளை எழுதுங்கள்\n"
        "👉 அவசர நிலைகள் உடனே உயர்நிலை அதிகாரிக்கு தெரிவிக்கப்படும்",
        parse_mode="Markdown"
    )

# =========================
# 💬 MESSAGE HANDLER
# =========================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip().lower()

    if user_text in ["சரி", "ok", "okay"]:
        mark_responded(update.effective_chat.id)
        await update.message.reply_text("🙏 நல்லது. கவனித்துக் கொள்ளுங்கள்.")
        return

    if user_text in ["சரி இல்லை", "not ok", "worse"]:
        await update.message.reply_text(
            "⚠️ நிலை மோசமாக உள்ளது.\n👉 உடனடியாக அரசு மருத்துவமனைக்கு அனுப்பவும்."
        )
        return

    tamil_text = normalize_input(user_text)
    duration = extract_duration(user_text)
    result = local_medical_ai(tamil_text, duration)

    await update.message.reply_text(result["reply"])

    log_visit(
        chat_id=update.effective_chat.id,
        symptoms=user_text,
        issue=result["issue"],
        duration_days=duration,
        advice=result["advice"]
    )

    if result["issue"] == "emergency":
        await notify_manager(context, {
            "chat_id": update.effective_chat.id,
            "symptoms": user_text,
            "duration": duration or "Unknown"
        })
        context.job_queue.run_once(
            escalate_if_no_response,
            when=3600,
            data={
                "chat_id": update.effective_chat.id,
                "symptoms": user_text,
                "duration": duration or "Unknown"
            }
        )

# =========================
# 🚀 MAIN
# =========================
def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("✅ ASHA Sahayi bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
