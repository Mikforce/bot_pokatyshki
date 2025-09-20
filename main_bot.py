import logging
import asyncio
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from message_analyzer import analyze_message

# Загрузка переменных окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация из .env
BOT_TOKEN = os.getenv('BOT_TOKEN')
YOUR_TELEGRAM_ID = int(os.getenv('YOUR_TELEGRAM_ID'))

# Парсим CHAT_IDS из строки в список чисел
CHAT_IDS_STR = os.getenv('CHAT_IDS', '').strip()
CHAT_IDS = []
if CHAT_IDS_STR:
    try:
        # Убираем возможные квадратные скобки и пробелы
        clean_str = CHAT_IDS_STR.replace('[', '').replace(']', '').replace(' ', '')
        if clean_str:  # Проверяем не пустая ли строка после очистки
            CHAT_IDS = [int(chat_id.strip()) for chat_id in clean_str.split(',') if chat_id.strip()]
    except ValueError as e:
        logger.error(f"❌ Ошибка парсинга CHAT_IDS: {e}")
        CHAT_IDS = []

# Валидация конфигурации
if not BOT_TOKEN or BOT_TOKEN == 'your_actual_bot_token_here':
    logger.error("❌ BOT_TOKEN не установлен в .env файле")
    exit(1)

if not YOUR_TELEGRAM_ID:
    logger.error("❌ YOUR_TELEGRAM_ID не установлен в .env файле")
    exit(1)

logger.info(f"✅ Конфигурация загружена: TG_ID={YOUR_TELEGRAM_ID}, CHAT_IDS={CHAT_IDS}")


async def send_telegram_alert(context: ContextTypes.DEFAULT_TYPE, alert_text: str):
    """Отправляет уведомление в личные сообщения Telegram."""
    try:
        await context.bot.send_message(
            chat_id=YOUR_TELEGRAM_ID,
            text=alert_text,
            parse_mode='Markdown'
        )
        logger.info("✅ Уведомление отправлено успешно")
    except Exception as e:
        logger.error(f"❌ Ошибка отправки уведомления: {e}")


async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Эта функция вызывается на каждое новое сообщение в чате."""
    # Проверяем, из нужного ли нам чата сообщение
    if CHAT_IDS and update.effective_chat.id not in CHAT_IDS:
        return

    # Получаем текст сообщения
    message_text = update.message.text
    if not message_text:
        return  # Игнорируем стикеры, фото и т.д.

    user = update.message.from_user
    chat_title = update.effective_chat.title or "Unknown"

    logger.info(f"💬 Сообщение от {user.first_name} в чате '{chat_title}': {message_text[:50]}...")

    # Анализируем сообщение нашей ML-моделью
    is_ride_event, confidence = analyze_message(message_text)

    # Если модель уверена, что это предложение покататься - действуем!
    if is_ride_event and confidence > 0.7:
        alert_text = (
            f"🚨 *Обнаружено предложение покататься!*\n\n"
            f"*Чат:* {chat_title}\n"
            f"*Пользователь:* {user.full_name} (@{user.username})\n"
            f"*Уверенность модели:* {confidence:.2%}\n\n"
            f"*Сообщение:*\n_{message_text}_\n\n"
            f"[➡️ Перейти к сообщению](https://t.me/c/{str(update.effective_chat.id).replace('-100', '')}/{update.message.id})"
        )

        logger.warning(f"🎯 Обнаружено событие! Уверенность: {confidence:.2%}")

        # Отправляем уведомление в Telegram
        await send_telegram_alert(context, alert_text)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок."""
    logger.error(f"❌ Ошибка при обработке update {update}: {context.error}")


def main():
    """Запуск основного бота с NLP."""
    # Создаем Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчик для текстовых сообщений в группах/супергруппах
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.IS_AUTOMATIC_FORWARD & filters.ChatType.GROUPS,
        check_message
    ))

    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)

    # Запускаем бота
    logger.info("🤖 Основной бот с NLP запущен!")
    logger.info("📍 Отслеживаемые чаты: %s", CHAT_IDS if CHAT_IDS else "ВСЕ чаты")
    logger.info("✅ Бот готов к работе и анализу сообщений...")

    application.run_polling()


if __name__ == '__main__':
    main()