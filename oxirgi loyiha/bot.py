import os
import django

# Django settings ni sozlash
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # config = sizning Django loyihangiz nomi
django.setup()



from asgiref.sync import sync_to_async
from users.models import User
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    username = update.effective_user.username
    full_name = update.effective_user.full_name

    # ORM chaqiruvini async kontekstda ishlatish
    user, created = await sync_to_async(User.objects.get_or_create)(
        telegram_id=chat_id,
        defaults={
            'username': username,
            'full_name': full_name
        }
    )

    # Database dan qayta olish
    user_from_db = await sync_to_async(User.objects.get)(telegram_id=chat_id)

    # Userga ma’lumot yuborish
    await update.message.reply_text(
        f"Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz!\n\n"
        f"ID: {user_from_db.telegram_id}\n"
        f"Ism: {user_from_db.full_name}\n"
        f"Username: @{user_from_db.username}"
    )

# Botni ishga tushirish
if __name__ == "__main__":
    TOKEN = "8621705819:AAGsFrxnTKMtJcbvSHmqNvz_vblzlIEHNuY"  # Bu yerga Telegram bot tokeningizni qo'ying
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Bot ishga tushdi...")
    app.run_polling()