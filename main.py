import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Ваш токен от BotFather
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Клавиатура с кнопками
def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("📋 Услуги и Цены")],
        [KeyboardButton("🏠 Наши работы")],
        [KeyboardButton("📞 Связаться с нами")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Здравствуйте! 👋\n"
        "Мы специализируемся на строительстве загородных домов в Ленинградской области.\n\n"
        "Выберите, что вас интересует:"
    )
    await update.message.reply_text(welcome_text, reply_markup=main_menu_keyboard())

# Обработчик кнопки "Услуги и Цены"
async def services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    services_text = (
        "🏗️ <b>Наши основные услуги:</b>\n\n"
        "• Полный цикл строительства 'под ключ'\n"
        "• Фундаменты (ленточные, свайно-ростверковые, УШП)\n"
        "• Каркасные дома\n"
        "• Дома из газобетона\n"
        "• Бани и хозпостройки\n\n"
        "💎 <b>Примерный расчет цены:</b>\n"
        "Каркасный дом: от 35 000 руб/м²\n"
        "Дом из газобетона: от 45 000 руб/м²\n\n"
        "<i>Точная стоимость рассчитывается индивидуально после консультации и замера.</i>"
    )
    await update.message.reply_text(services_text, parse_mode='HTML')

# Обработчик кнопки "Наши работы"
async def portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    portfolio_text = "Здесь будут фотографии наших построенных объектов. Пока что раздел в разработке."
    await update.message.reply_text(portfolio_text)

# Обработчик кнопки "Связаться с нами"
async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_text = (
        "Чтобы мы могли оперативно связаться с вами для консультации и замера, пожалуйста, поделитесь вашим номером телефона.\n\n"
        "Нажмите кнопку ниже 👇"
    )
    contact_keyboard = ReplyKeyboardMarkup([[KeyboardButton("📲 Отправить номер", request_contact=True)]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(contact_text, reply_markup=contact_keyboard)

# Обработчик получения контакта
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    user = update.message.from_user
    
    # Сообщение для админа (вас)
    admin_text = (
        "🔥 <b>НОВАЯ ЗАЯВКА!</b>\n\n"
        f"Имя: {contact.first_name}\n"
        f"Телефон: +{contact.phone_number}\n"
        f"Username: @{user.username if user.username else 'не указан'}"
    )
    
    # Отправляем заявку вам в личку
    # ЗАМЕНИТЕ 1234567890 НА ВАШ ТЕЛЕГРАМ ID (я позже скажу, как его узнать)
    admin_chat_id = "382053386"
    try:
        await context.bot.send_message(chat_id=admin_chat_id, text=admin_text, parse_mode='HTML')
        await update.message.reply_text("✅ Спасибо! Мы получили ваш номер и свяжемся с вами в ближайшее время!", reply_markup=main_menu_keyboard())
    except Exception as e:
        logger.error(f"Ошибка отправки заявки: {e}")
        await update.message.reply_text("✅ Спасибо! Мы свяжемся с вами скоро.", reply_markup=main_menu_keyboard())

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📋 Услуги и Цены":
        await services(update, context)
    elif text == "🏠 Наши работы":
        await portfolio(update, context)
    elif text == "📞 Связаться с нами":
        await contact(update, context)
    else:
        await update.message.reply_text("Пожалуйста, используйте кнопки меню 👇", reply_markup=main_menu_keyboard())

def main():
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    
    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':

    main()
