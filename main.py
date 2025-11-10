import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Ваш токен от BotFather
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Ваш Telegram ID
ADMIN_CHAT_ID = "382053386"

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
    # Сначала отправляем текст
    portfolio_text = (
        "🏠 <b>Наши реализованные проекты</b>\n\n"
        "Вот примеры домов, которые мы построили для наших клиентов в Ленинградской области. "
        "Каждый проект индивидуален и адаптирован под потребности заказчика."
    )
    await update.message.reply_text(portfolio_text, parse_mode='HTML')
    
    # Затем отправляем медиагруппу с фото
    try:
        photo_urls = [
            "https://i.ibb.co/4ZXhSST1/photo1.jpg",
            "https://i.ibb.co/xtFqYxv4/photo2.jpg", 
            "https://i.ibb.co/SD0ZFh67/photo3.jpg",
            "https://i.ibb.co/MyypsSK4/photo4.jpg",
            "https://i.ibb.co/Kj0LQBwH/photo5.jpg",
            "https://i.ibb.co/FLjYpTC9/photo6.jpg"
        ]
        
        # Делим на группы по 4 фото
        group1 = photo_urls[:4]
        group2 = photo_urls[4:]
        
        # Отправляем первую группу
        media_group1 = []
        for i, url in enumerate(group1):
            caption = "🏡 Наши проекты - каркасные дома и дома из газобетона" if i == 0 else ""
            media_group1.append(InputMediaPhoto(media=url, caption=caption))
        
        await update.message.reply_media_group(media=media_group1)
        
        # Если есть вторая группа - отправляем её
        if group2:
            media_group2 = []
            for url in group2:
                media_group2.append(InputMediaPhoto(media=url))
            await update.message.reply_media_group(media=media_group2)
        
    except Exception as e:
        logger.error(f"Ошибка отправки фото: {e}")
        await update.message.reply_text("⚠️ Фотографии временно недоступны. Приносим извинения!")

# Обработчик кнопки "Связаться с нами"
async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Пользователь нажал 'Связаться с нами'")
    contact_text = (
        "Чтобы мы могли оперативно связаться с вами для консультации и замера, пожалуйста, поделитесь вашим номером телефона.\n\n"
        "Нажмите кнопку ниже 👇"
    )
    contact_keyboard = ReplyKeyboardMarkup([[KeyboardButton("📲 Отправить номер", request_contact=True)]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(contact_text, reply_markup=contact_keyboard)

# Обработчик получения контакта
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("=== ПОЛУЧЕН КОНТАКТ! ===")
    
    contact = update.message.contact
    user = update.message.from_user
    
    logger.info(f"Контакт: {contact.first_name}, тел: +{contact.phone_number}")
    logger.info(f"Пользователь: {user.username}, ID: {user.id}")
    
    # Сообщение для админа
    admin_text = (
        "
