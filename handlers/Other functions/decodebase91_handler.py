from botcfg import bot
from dp import conn_bot
import base91
import binascii
import time

@bot.message_handler(commands=['decode_base91'])
def decode_base91_message(message):
    cur_bot = conn_bot.cursor()
    text_parts = message.text.split(' ', maxsplit=1)

    if len(text_parts) < 2:
        bot.send_message(message.chat.id, "❌ Напиши текст після /decode_base91")
        return
    
    original_text = text_parts[1]
    try:
        decoded_text = base91.decode(original_text).decode()
    except binascii.Error:
        bot.send_message(message.chat.id, "❌ Ви ввели текст, який не є зашифрованим у форматі Base91. Будь ласка, введіть коректне зашифроване повідомлення! 😅")
        return
    except UnicodeDecodeError:
        bot.send_message(message.chat.id, "❌ Розшифровані дані не є текстом у форматі UTF-8. Спробуйте інше повідомлення! 😅")
        return
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Помилка: {e}. Спробуйте ще раз! 😅")
        return

    timestamp = int(time.time())
    cur_bot.execute("INSERT INTO messages (user_id, message_encoded, message_decoded, timestamp) VALUES (?, ?, ?, ?)", 
                    (message.from_user.id, original_text, decoded_text, timestamp))
    conn_bot.commit()

    bot.send_message(message.chat.id, f"🔓 Розшифровано:\n`{decoded_text}`", parse_mode="Markdown")
