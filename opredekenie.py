# import logging
# import os
# from dotenv import load_dotenv
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
#
# # Загрузка переменных окружения из .env файла
# load_dotenv()
#
# # Настройка логирования
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )
# logger = logging.getLogger(__name__)
#
# # Конфигурация из .env
# BOT_TOKEN = os.getenv('BOT_TOKEN') or 'YOUR_BOT_TOKEN_HERE'
#
#
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Обработчик команды /start."""
#     await update.message.reply_text(
#         "👋 Привет! Я бот для определения ID чатов.\n\n"
#         "Просто добавьте меня в любой чат и напишите:\n"
#         "• `/id` - чтобы получить ID этого чата\n"
#         "• `/info` - подробная информация о чате\n\n"
#         "ID чата понадобится для настройки основного бота!"
#     )
#
#
# async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Команда для получения ID чата."""
#     chat = update.effective_chat
#     user = update.effective_user
#
#     response = (
#         f"📋 *ID чата:* `{chat.id}`\n"
#         f"👤 *Ваш ID:* `{user.id}`\n"
#         f"💬 *Тип чата:* {chat.type}\n"
#     )
#
#     if chat.title:
#         response += f"🏷️ *Название чата:* {chat.title}\n"
#
#     if chat.username:
#         response += f"🔗 *Username:* @{chat.username}\n"
#
#     response += "\n💡 *Скопируйте ID чата в файл .env:*\n"
#     response += f"`CHAT_IDS={chat.id}`"
#
#     await update.message.reply_text(response, parse_mode='Markdown')
#
#
# async def get_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Подробная информация о чате."""
#     chat = update.effective_chat
#     user = update.effective_user
#
#     # Основная информация
#     info_text = (
#         f"🔍 *Детальная информация:*\n\n"
#         f"*Чат:*\n"
#         f"• ID: `{chat.id}`\n"
#         f"• Тип: {chat.type}\n"
#     )
#
#     if chat.title:
#         info_text += f"• Название: {chat.title}\n"
#     if chat.username:
#         info_text += f"• Username: @{chat.username}\n"
#     if chat.description:
#         info_text += f"• Описание: {chat.description}\n"
#
#     info_text += f"\n*Вы:*\n• ID: `{user.id}`\n• Имя: {user.full_name}\n"
#     if user.username:
#         info_text += f"• Username: @{user.username}\n"
#
#     # Дополнительная информация для групп
#     if chat.type in ["group", "supergroup"]:
#         info_text += f"\n*Для .env файла:*\n`CHAT_IDS={chat.id}`\n\n"
#         info_text += "📝 *Добавьте эту строку в файл .env основного бота*"
#
#     await update.message.reply_text(info_text, parse_mode='Markdown')
#
#
# async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Обработчик ошибок."""
#     logger.error(f"Ошибка при обработке update {update}: {context.error}")
#
#
# def main():
#     """Запуск бота для определения ID чатов."""
#     # Создаем Application
#     application = Application.builder().token(BOT_TOKEN).build()
#
#     # Добавляем обработчики команд
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CommandHandler("id", get_id))
#     application.add_handler(CommandHandler("info", get_info))
#     application.add_handler(CommandHandler("chatid", get_id))  # Алиас
#
#     # Добавляем обработчик ошибок
#     application.add_error_handler(error_handler)
#
#     # Запускаем бота
#     logger.info("Бот для определения ID чатов запущен!")
#     logger.info("Добавьте бота в чат и используйте команды:")
#     logger.info("/id - получить ID чата")
#     logger.info("/info - подробная информация")
#
#     application.run_polling()
#
#
# if __name__ == '__main__':
#     main()


import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

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


async def delete_specific_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет конкретное сообщение бота в чате 'Ижовые рукавицы'."""
    try:
        # Данные для удаления
        CHAT_ID = -4264685397  # ID чата "Ижовые рукавицы"
        MESSAGE_ID = update.message.message_id - 1  # ID сообщения для удаления (предыдущее)

        # Пытаемся удалить сообщение
        await context.bot.delete_message(chat_id=CHAT_ID, message_id=MESSAGE_ID)

        # Подтверждаем удаление
        response = await update.message.reply_text(
            "✅ Сообщение успешно удалено из чата 'Ижовые рукавицы'"
        )

        # Удаляем и это подтверждение через 5 секунд
        await asyncio.sleep(5)
        await response.delete()

    except Exception as e:
        error_msg = f"❌ Ошибка при удалении: {e}"
        await update.message.reply_text(error_msg)
        logger.error(error_msg)


async def delete_by_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет сообщение по конкретному ID."""
    try:
        if not context.args:
            await update.message.reply_text("❌ Укажите ID сообщения: /delete_id <message_id>")
            return

        message_id = int(context.args[0])
        CHAT_ID = -4264685397  # ID чата "Ижовые рукавицы"

        await context.bot.delete_message(chat_id=CHAT_ID, message_id=message_id)
        response = await update.message.reply_text(f"✅ Сообщение {message_id} удалено")

        await asyncio.sleep(5)
        await response.delete()

    except ValueError:
        await update.message.reply_text("❌ ID сообщения должен быть числом")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")


async def list_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает последние сообщения бота."""
    try:
        CHAT_ID = -4264685397

        # Получаем информацию о чате
        chat = await context.bot.get_chat(CHAT_ID)
        await update.message.reply_text(
            f"💬 Чат: {chat.title}\n"
            f"🆔 ID: {CHAT_ID}\n\n"
            "Для удаления сообщения используйте:\n"
            "• /delete - удалить предыдущее сообщение\n"
            "• /delete_id <number> - удалить по ID\n"
            "• Попросите администратора удалить вручную"
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок."""
    logger.error(f"Ошибка: {context.error}")


def main():
    """Запуск бота для удаления сообщений."""
    # Создаем Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("delete", delete_specific_message))
    application.add_handler(CommandHandler("delete_id", delete_by_id))
    application.add_handler(CommandHandler("list", list_messages))
    application.add_handler(CommandHandler("start", list_messages))

    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)

    # Запускаем бота
    logger.info("🤖 Бот для удаления сообщений запущен!")
    logger.info("💬 Команды:")
    logger.info("   /delete - удалить предыдущее сообщение")
    logger.info("   /delete_id <number> - удалить по ID")
    logger.info("   /list - информация о чате")

    application.run_polling()


if __name__ == '__main__':
    main()