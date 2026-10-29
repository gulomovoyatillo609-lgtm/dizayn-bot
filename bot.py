import telebot
import requests

# Telegram bot tokeningiz
TELEGRAM_BOT_TOKEN = "9160950331:AAGoPVgSJz-SDEY0Xx4aWsuOAtVSpDveDsc"

# DeepSeek API kalitingiz
DEEPSEEK_API_KEY = "sk-fdc985eaf835475ab02cf35b645581e6"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Menejer botning vazifasi va narxlar ro'yxati
SYSTEM_PROMPT = """
Sen professional grafik dizaynerning shaxsiy menejer botisan. 

Asosiy vazifang:
1. Mijozlar bilan xushmuomala, samimiy va o'zbek tilida muloqot qilish.
2. Mijoz so'ragan xizmat turi bo'yicha quyidagi prayst-list asosida aniq ma'lumot berish.
3. Buyurtma bermoqchi bo'lgan mijozdan: qanday dizayn kerakligi, texnik topshiriq (ma'lumotlar), qachonga tayyor bo'lishi kerakligi hamda bog'lanish uchun telefon raqami yoki Telegram profilini so'rash.
4. Javoblarni juda uzun qilmasdan, aniq, tushunarli va chiroyli formatda yozish.

XIZMATLAR VA NARXLAR RO'YXATI:
- Reklama bannerlari: 300 000 so'mdan boshlanadi (hajmi va murakkabligiga qarab narxi o'zgarishi mumkin).
- SMM post (1 talik): 100 000 so'm.
- Karusel post dizayni: 180 000 so'mdan boshlanadi.
- Video Reels uchun muqova (cover) dizayn: 50 000 so'mdan (doimiy mijozlar uchun va soni ko'p bo'lsa, narxi kelishiladi).
- Infografika dizaynlari: 80 000 so'mdan boshlanadi.
- Logotip (ijtimoiy tarmoqlar uchun): 500 000 so'mdan boshlanadi.
- Kattaroq brendlar uchun logotip (barcha kerakli ishchi fayllari bilan): 100$ dan 500$ gacha (yoki loyiha holatiga qarab kelishiladi).
- Katalog dizayni: 1 ta sahifasi (page) 80 000 so'mdan (sahifalar soni ko'p bo'lsa, narxi kelishiladi).
- Flayer va broshyura dizayni: 150 000 so'mdan 500 000 so'mgacha.

MUHIM ESLATMA:
- Bizda "3D mahsulot vizualizatsiyasi" xizmati YO'Q. Agar mijoz 3D dizayn yoki 3D vizualizatsiya so'rasa, bu xizmat bizda mavjud emasligini xushmuomalalik bilan tushuntir va boshqa grafik dizayn xizmatlarimizni taklif qil.
"""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "Assalomu alaykum! Men Grafik dizaynerning shaxsiy menejer botiman. 🎨\n\n"
        "Sizga SMM postlar, logotip, banner, katalog yoki boshqa dizayn xizmatlari kerakmi?\n"
        "Marhamat, o'zingizni qiziqtirgan savolni yozing yoki narxlar bilan tanishing!"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def chat_with_deepseek(message):
    user_message = message.text
    
    # Mijozga "yozmoqda..." (typing) holatini ko'rsatish
    bot.send_chat_action(message.chat.id, 'typing')
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.5
    }
    
    try:
        response = requests.post(
            "https://api.deepseek.com/chat/completions", 
            headers=headers, 
            json=data, 
            timeout=30
        )
        response.raise_for_status()
        res_json = response.json()
        bot_reply = res_json['choices'][0]['message']['content']
        bot.reply_to(message, bot_reply)
        
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        bot.reply_to(message, f"Xatolik sababi: {e}")

if __name__ == "__main__":
    print("Menejer bot ishga tushdi...")
    bot.infinity_polling()
