import telebot
import requests

# Telegram bot tokeningiz
TELEGRAM_BOT_TOKEN = "9160950331:AAGoPVgSJz-SDEY0Xx4aWsuOAtVSpDveDsc"

# Dizaynbot uchun Gemini API kalitingiz
GEMINI_API_KEY = "AQ.Ab8RN6J5HO1h6kELSSWfxKD1_NJpdr1rBJb08vW4XPlodPo3Mg"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

XIZMATLAR_MATNI = (
    "💼 **Grafik dizayn xizmatlari va narxlar:**\n\n"
    "• **SMD post va reklama bannerlari:** 50,000 so'mdan boshlab\n"
    "• **Tashqi reklama (bilbord, panno, shtender):** 80,000 so'mdan boshlab\n"
    "• **Mahsulot katalogi va bukletlar:** 1 sahifasi 40,000 so'mdan boshlab\n"
    "• **Flayer, vizitka va poligrafiya:** 50,000 so'mdan boshlab\n"
    "• **Logotip va brending:** Kelishilgan holda\n\n"
    "📌 *Aniq narx ish hajmi va texnik topshiriqqa (TZ) qarab belgilanadi.*"
)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "Assalomu alaykum! Men grafik dizayner Oyatilloning rasmiy yordamchi menejer botiman. 🎨\n\n"
        "Sizga quyidagi yo'nalishlarda professional dizayn xizmatlarini taklif qilamiz:\n"
        "• Reklama bannerlari va SMD postlar\n"
        "• Kataloglar, bukletlar va poligrafiya dizayni\n"
        "• Tashqi reklama va brending materiallari\n\n"
        "📋 Xizmatlar va narxlar bilan tanishish uchun /xizmatlar buyrug'ini bosing yoki savolingizni yozib qoldiring!"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['xizmatlar', 'narxlar'])
def send_services(message):
    bot.reply_to(message, XIZMATLAR_MATNI, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def chat_with_gemini(message):
    user_message = message.text
    
    system_instruction = (
        "Sen Oyatillo ismli professional grafik dizaynerning Telegramdagi AI menejerisan. "
        "Mijozlarga xushmuomala, qisqa, aniq va professional tarzda o'zbek tilida javob ber. "
        "MUHIM QOIDALAR:\n"
        "1. Oyatillo 3D render yoki 3D modellashtirish qilmaydi (faqat 2D grafik dizayn, poligrafiya, kataloglar, SMD va tashqi reklama bannerlari).\n"
        "2. Hech qachon kompaniya yoki brend nomini (masalan, ELITE) qo'shib gapirma, Oyatillo mustaqil dizayner sifatida ishlaydi.\n"
        "3. Narxlar so'ralsa quyidagilarni ayt: SMD/reklama bannerlari 50,000 so'mdan, tashqi reklama 80,000 so'mdan, katalog sahifasi 40,000 so'mdan, poligrafiya 50,000 so'mdan boshlanadi.\n"
        "4. Mijoz buyurtma bermoqchi bo'lsa, undan: 1) Qanday dizayn kerakligi, 2) O'lchamlari va matni (TZ), 3) Telefon raqami yoki Telegram lichkasini qoldirishni so'ra."
    )
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }
    
    payload = {
        "system_instruction": {
            "parts": [{"text": system_instruction}]
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_message}]
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        res_json = response.json()
        
        if "candidates" in res_json:
            bot_reply = res_json["candidates"][0]["content"]["parts"][0]["text"]
            bot.reply_to(message, bot_reply)
        else:
            print("Gemini API xatosi:", res_json)
            bot.reply_to(message, "Kechirasiz, tizimda kichik uzilish bo'ldi. Savolingizni qayta yuboring.")
    except Exception as e:
        print("Xatolik:", e)
        bot.reply_to(message, "Kechirasiz, javob berishda vaqtincha xatolik yuz berdi. Birozdan so'ng urinib ko'ring.")

if __name__ == "__main__":
    print("Gemini menejer bot ishga tushdi...")
    bot.infinity_polling()
