# # users/management/commands/runbot.py
# from django.core.management.base import BaseCommand
# from django.urls import reverse
# from telegram.ext import Application, CommandHandler
# from telegram import Update
# from telegram.ext import CommandHandler, ContextTypes
# from django.contrib.auth.models import User
# from users.models import TelegramProfile
#
# # users/management/commands/runbot.py
#
# from telegram import Update
# from telegram.ext import CommandHandler, ContextTypes
# from django.contrib.auth.models import User
# from users.models import TelegramProfile
# from asgiref.sync import sync_to_async
#
#
# TOKEN = '7178817143:AAHUPv-Bkmlfawk1UK2BmMT263ATIgUoghM'
#
# class Command(BaseCommand):
#     help = 'Start the Telegram bot'
#
#     def handle(self, *args, **kwargs):
#         application = Application.builder().token(TOKEN).build()
#
#         async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#             telegram_id = update.message.from_user.id
#             profile = await sync_to_async(TelegramProfile.objects.get)(telegram_id=telegram_id)
#             await sync_to_async(profile.generate_otp_code)()
#
#             await update.message.reply_text(
#                 f"Your OTP code is: {profile.otp_code}. Please enter this on the website to login.")
#
#         application.add_handler(CommandHandler("login", login_command))
#
#         async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#             telegram_id = update.message.from_user.id
#             username = update.message.from_user.username
#
#             # Foydalanuvchini asinxron kontekstda yaratish yoki topish
#             user, _ = await sync_to_async(User.objects.get_or_create)(
#                 username=username, defaults={'password': 'telegram_password'}
#             )
#             profile, _ = await sync_to_async(TelegramProfile.objects.get_or_create)(
#                 user=user, telegram_id=telegram_id
#             )
#             await sync_to_async(profile.generate_auth_token)()
#
#             # reverse() yordamida URL manzilini to'g'ri yarating
#
#             login_url = reverse('telegram_login', kwargs={'token': profile.auth_token})
#             full_url = f"http://127.0.0.1:8000{login_url}"
#             await update.message.reply_text(f"Click the link to login: {profile.auth_token}")
#
#         application.add_handler(CommandHandler("login", start))
#         application.run_polling()
#
#         async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
#             message = "Menu:\n1. Login\n2. Help\n3. Order Status\n4. Contact Support"
#             await update.message.reply_text(message)
#
#         application.add_handler(CommandHandler("menu", menu))


#
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# from django.core.management.base import BaseCommand
# from users.models import TelegramProfile, User
# from django.urls import reverse
# from asgiref.sync import sync_to_async
#
# TOKEN = '7178817143:AAHUPv-Bkmlfawk1UK2BmMT263ATIgUoghM'
#
# class Command(BaseCommand):
#     help = 'Start the Telegram bot'
#
#     def handle(self, *args, **kwargs):
#         application = Application.builder().token(TOKEN).build()
#
#         async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#             telegram_id = update.message.from_user.id
#             username = update.message.from_user.username or f'tg_user_{telegram_id}'
#
#             user, _ = await sync_to_async(User.objects.get_or_create)(username=username, defaults={'password': 'telegram_password'})
#             profile, created = await sync_to_async(TelegramProfile.objects.get_or_create)(telegram_id=telegram_id, defaults={'user': user})
#
#             if created or not profile.full_name or not profile.phone_number:
#                 await update.message.reply_text("Welcome! Please provide your full name:")
#                 context.user_data['state'] = 'waiting_for_full_name'
#                 return
#
#             await sync_to_async(profile.generate_auth_token)()
#             login_url = reverse('telegram_login', kwargs={'token': profile.generate_otp_code})
#             full_url = f"http://127.0.0.1:8000{login_url}"
#             await update.message.reply_text(f"Click the link to login: {full_url}")
#
#         async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#             telegram_id = update.message.from_user.id
#             profile = await sync_to_async(TelegramProfile.objects.get)(telegram_id=telegram_id)
#
#             state = context.user_data.get('state')
#
#             if state == 'waiting_for_full_name':
#                 profile.full_name = update.message.text
#                 await sync_to_async(profile.save)()
#                 await update.message.reply_text("Great! Now, please provide your phone number:")
#                 context.user_data['state'] = 'waiting_for_phone_number'
#
#             elif state == 'waiting_for_phone_number':
#                 profile.phone_number = update.message.text
#                 await sync_to_async(profile.save)()
#                 await sync_to_async(profile.generate_otp_code)()
#                 login_url = reverse('telegram_login', kwargs={'token': profile.otp_code})
#                 full_url = f"http://127.0.0.1:8000{login_url}"
#                 await update.message.reply_text(f"Thank you! Now you can login: {full_url}")
#                 context.user_data['state'] = None
#
#             else:
#                 await update.message.reply_text("I'm not sure what you mean. Please use the commands.")
#
#         async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#             telegram_id = update.message.from_user.id
#             profile = await sync_to_async(TelegramProfile.objects.get)(telegram_id=telegram_id)
#             await sync_to_async(profile.generate_otp_code)()
#             await update.message.reply_text(
#                 f"Your OTP code is: {profile.otp_code}. Please enter this on the website to login."
#             )
#
#         application.add_handler(CommandHandler("start", start))
#         application.add_handler(CommandHandler("login", login_command))
#         application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
#
#         application.run_polling()













#
# from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# from django.core.management.base import BaseCommand
# from users.models import TelegramProfile, User
# from django.urls import reverse
# from asgiref.sync import sync_to_async
#
# TOKEN = '7178817143:AAHUPv-Bkmlfawk1UK2BmMT263ATIgUoghM'
#
# class Command(BaseCommand):
#     help = 'Start the Telegram bot'
#
#     def handle(self, *args, **kwargs):
#         application = Application.builder().token(TOKEN).build()
#
#         async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#             telegram_id = update.message.from_user.id
#             username = update.message.from_user.username or f'tg_user_{telegram_id}'
#
#             user, _ = await sync_to_async(User.objects.get_or_create)(username=username, defaults={'password': 'telegram_password'})
#             profile, created = await sync_to_async(TelegramProfile.objects.get_or_create)(telegram_id=telegram_id, defaults={'user': user})
#
#             if created or not profile.full_name or not profile.phone_number:
#                 # Send a button for sharing contact info
#                 contact_button = KeyboardButton(text="Share Contact", request_contact=True)
#                 reply_markup = ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True)
#                 await update.message.reply_text("Welcome! Please share your contact information:", reply_markup=reply_markup)
#                 context.user_data['state'] = 'waiting_for_contact'
#                 return
#
#             await sync_to_async(profile.generate_auth_token)()
#             await update.message.reply_text(f"Click the link to login: {profile.otp_code}")
#
#         async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#             telegram_id = update.message.from_user.id
#             profile = await sync_to_async(TelegramProfile.objects.get)(telegram_id=telegram_id)
#
#             state = context.user_data.get('state')
#
#             if state == 'waiting_for_contact' and update.message.contact:
#                 contact = update.message.contact
#                 profile.full_name = f"{contact.first_name} {contact.last_name or ''}".strip()
#                 profile.phone_number = contact.phone_number
#                 await sync_to_async(profile.save)()
#                 await sync_to_async(profile.generate_otp_code)()
#                 # await update.message.reply_text(f"Thank you! Now you can login: {profile.otp_code}")
#
#                 code_text = f"Code: {profile.otp_code}"
#                 renew_button = InlineKeyboardButton("Yangilash / Renew", callback_data='renew_otp')
#                 reply_markup = InlineKeyboardMarkup([[renew_button]])
#                 await update.message.reply_text(code_text, reply_markup=reply_markup)
#
#                 context.user_data['state'] = None
#             else:
#                 await update.message.reply_text("Please share your contact information using the button provided.")
#
#         async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#             telegram_id = update.message.from_user.id
#             profile = await sync_to_async(TelegramProfile.objects.get)(telegram_id=telegram_id)
#             # await sync_to_async(profile.generate_otp_code)()
#             # await update.message.reply_text(
#             #     f"Your OTP code is: {profile.otp_code}. Please enter this on the website to login."
#             # )
#             code_text = f"Code: {profile.otp_code}"
#             renew_button = InlineKeyboardButton("Yangilash / Renew", callback_data='renew_otp')
#             reply_markup = InlineKeyboardMarkup([[renew_button]])
#             await update.message.reply_text(code_text, reply_markup=reply_markup)
#
#         application.add_handler(CommandHandler("start", start))
#         application.add_handler(CommandHandler("login", login_command))
#         application.add_handler(MessageHandler(filters.CONTACT, handle_message))
#         application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
#
#         application.run_polling()









from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from django.core.management.base import BaseCommand
from users.models import TelegramProfile, User
from django.urls import reverse
from asgiref.sync import sync_to_async

# TOKEN = '7178817143:AAHUPv-Bkmlfawk1UK2BmMT263ATIgUoghM'         #foodme_robot
TOKEN = '6993043220:AAFeGm6BZjYyNOlP5WO40ulD9yWrBh7_nXI'           #sinov

class Command(BaseCommand):
    help = 'Start the Telegram bot'

    def handle(self, *args, **kwargs):
        application = Application.builder().token(TOKEN).build()

        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            telegram_id = update.message.from_user.id
            username = update.message.from_user.username or f'tg_user_{telegram_id}'

            user, _ = await sync_to_async(User.objects.get_or_create)(username=username, defaults={'password': 'telegram_password'})
            profile, created = await sync_to_async(TelegramProfile.objects.get_or_create)(telegram_id=telegram_id, defaults={'user': user})

            if created or not profile.full_name or not profile.phone_number:
                # Contact info olish uchun tugma
                contact_button = KeyboardButton(text="Share Contact", request_contact=True)
                reply_markup = ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True)
                await update.message.reply_text("Welcome! Please share your contact information:", reply_markup=reply_markup)
                context.user_data['state'] = 'waiting_for_contact'
                return

            # OTP kodni inline tugma bilan jo'natish
            code_text = f"🔐 code: `{profile.otp_code}`"
            renew_button = InlineKeyboardButton("🔄 Yangilash / Renew", callback_data='renew_otp')
            reply_markup = InlineKeyboardMarkup([[renew_button]])
            await update.message.reply_text(code_text, reply_markup=reply_markup, parse_mode='MarkdownV2')

        async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
            telegram_id = update.message.from_user.id
            profile = await sync_to_async(TelegramProfile.objects.get)(telegram_id=telegram_id)

            state = context.user_data.get('state')

            if state == 'waiting_for_contact' and update.message.contact:
                contact = update.message.contact
                profile.full_name = f"{contact.first_name} {contact.last_name or ''}".strip()
                profile.phone_number = contact.phone_number
                await sync_to_async(profile.save)()
                await sync_to_async(profile.generate_otp_code)()

                # OTP kodni inline tugma bilan jo'natish
                code_text = f"🔐 code `{profile.otp_code}`"
                renew_button = InlineKeyboardButton("🔄 Yangilash / Renew", callback_data='renew_otp')
                reply_markup = InlineKeyboardMarkup([[renew_button]])
                await update.message.reply_text(code_text, reply_markup=reply_markup, parse_mode='MarkdownV2')

                context.user_data['state'] = None
            else:
                await update.message.reply_text("Please share your contact information using the button provided.")

        async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            telegram_id = update.message.from_user.id
            profile = await sync_to_async(TelegramProfile.objects.get)(telegram_id=telegram_id)
            await sync_to_async(profile.generate_otp_code)()

            # OTP kodni inline tugma bilan jo'natish
            code_text = f"🔐 code: `{profile.otp_code}`"
            renew_button = InlineKeyboardButton("🔄 Yangilash / Renew", callback_data='renew_otp')
            reply_markup = InlineKeyboardMarkup([[renew_button]])
            await update.message.reply_text(code_text, reply_markup=reply_markup, parse_mode='MarkdownV2')

        # Callback query ishlov beruvchi funksiya
        async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
            query = update.callback_query
            telegram_id = query.from_user.id
            profile = await sync_to_async(TelegramProfile.objects.get)(telegram_id=telegram_id)

            if await sync_to_async(profile.is_otp_valid)():
                await query.answer(text="👆 Eski kodingiz hali ham kuchda", show_alert=True)
            else:
                await sync_to_async(profile.generate_otp_code)()
                code_text = f"🔐 code: `{profile.otp_code}`"
                renew_button = InlineKeyboardButton("🔄 Yangilash / Renew", callback_data='renew_otp')
                reply_markup = InlineKeyboardMarkup([[renew_button]])
                await query.edit_message_text(text=code_text, reply_markup=reply_markup, parse_mode='MarkdownV2')

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("login", login_command))
        application.add_handler(MessageHandler(filters.CONTACT, handle_message))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_handler(CallbackQueryHandler(button))
        application.run_polling()



