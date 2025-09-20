import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Загрузка переменных окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация из .env
BOT_TOKEN = os.getenv('BOT_TOKEN') or 'YOUR_BOT_TOKEN_HERE'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start."""
    await update.message.reply_text(
        "👋 Привет! Я бот для определения ID чатов.\n\n"
        "Просто добавьте меня в любой чат и напишите:\n"
        "• `/id` - чтобы получить ID этого чата\n"
        "• `/info` - подробная информация о чате\n\n"
        "ID чата понадобится для настройки основного бота!"
    )


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для получения ID чата."""
    chat = update.effective_chat
    user = update.effective_user

    response = (
        f"📋 *ID чата:* `{chat.id}`\n"
        f"👤 *Ваш ID:* `{user.id}`\n"
        f"💬 *Тип чата:* {chat.type}\n"
    )

    if chat.title:
        response += f"🏷️ *Название чата:* {chat.title}\n"

    if chat.username:
        response += f"🔗 *Username:* @{chat.username}\n"

    response += "\n💡 *Скопируйте ID чата в файл .env:*\n"
    response += f"`CHAT_IDS={chat.id}`"

    await update.message.reply_text(response, parse_mode='Markdown')


async def get_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Подробная информация о чате."""
    chat = update.effective_chat
    user = update.effective_user

    # Основная информация
    info_text = (
        f"🔍 *Детальная информация:*\n\n"
        f"*Чат:*\n"
        f"• ID: `{chat.id}`\n"
        f"• Тип: {chat.type}\n"
    )

    if chat.title:
        info_text += f"• Название: {chat.title}\n"
    if chat.username:
        info_text += f"• Username: @{chat.username}\n"
    if chat.description:
        info_text += f"• Описание: {chat.description}\n"

    info_text += f"\n*Вы:*\n• ID: `{user.id}`\n• Имя: {user.full_name}\n"
    if user.username:
        info_text += f"• Username: @{user.username}\n"

    # Дополнительная информация для групп
    if chat.type in ["group", "supergroup"]:
        info_text += f"\n*Для .env файла:*\n`CHAT_IDS={chat.id}`\n\n"
        info_text += "📝 *Добавьте эту строку в файл .env основного бота*"

    await update.message.reply_text(info_text, parse_mode='Markdown')


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок."""
    logger.error(f"Ошибка при обработке update {update}: {context.error}")


def main():
    """Запуск бота для определения ID чатов."""
    # Создаем Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("id", get_id))
    application.add_handler(CommandHandler("info", get_info))
    application.add_handler(CommandHandler("chatid", get_id))  # Алиас

    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)

    # Запускаем бота
    logger.info("Бот для определения ID чатов запущен!")
    logger.info("Добавьте бота в чат и используйте команды:")
    logger.info("/id - получить ID чата")
    logger.info("/info - подробная информация")

    application.run_polling()


if __name__ == '__main__':
    main()