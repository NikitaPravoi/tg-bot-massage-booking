import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup, \
    InputMediaPhoto
from telegram.ext import ApplicationBuilder, Updater, CommandHandler, MessageHandler, filters, ConversationHandler,\
    CallbackContext, CallbackQueryHandler
import logging

# Словарь с типами массажей и временными слотами
massage_data = {
    "massage1": {
        "name": "Общий массаж всего тела",
        "duration": "70-80 мин",
        "price": "2000р",
        "times": [
            "9:00 - 10:20",
            "11:00 - 12:20",
            "14:00 - 15:20",
        ],
    },
    "massage2": {
        "name": "Релакс массаж",
        "duration": "60 мин",
        "price": "1300р",
        "times": [
            "10:00 - 11:00",
            "13:00 - 14:00",
            "15:30 - 16:30",
        ],
    },
    "massage3": {
        "name": "Массаж спины",
        "duration": "45 мин",
        "price": "1000р",
        "times": [
            "11:00 - 11:45",
            "14:30 - 15:15",
            "16:45 - 17:30",
        ],
    },
    "massage4": {
        "name": "Массаж шейно-воротниковой зоны",
        "duration": "30 мин",
        "price": "500р",
        "times": [
            "10:30 - 11:00",
            "13:45 - 14:15",
            "15:45 - 16:15",
        ],
    },
    "massage5": {
        "name": "Массаж ног",
        "duration": "30 мин",
        "price": "500р",
        "times": [
            "12:00 - 12:30",
            "14:45 - 15:15",
            "16:30 - 17:00",
        ],
    },
    "massage6": {
        "name": "Массаж рук",
        "duration": "30 мин",
        "price": "300р",
        "times": [
            "10:15 - 10:45",
            "13:15 - 13:45",
            "15:15 - 15:45",
        ],
    },
    "massage7": {
        "name": "Массаж головы",
        "duration": "20 мин",
        "price": "300р",
        "times": [
            "12:30 - 12:50",
            "14:00 - 14:20",
            "16:00 - 16:20",
        ],
    },
    "massage8": {
        "name": "Спина + ноги",
        "duration": "60 мин",
        "price": "1500р",
        "times": [
            "9:30 - 10:30",
            "13:30 - 14:30",
            "15:00 - 16:00",
        ],
    },
    "massage9": {
        "name": "Спина + шейно-воротниковая зона",
        "duration": "50 мин",
        "price": "1300р",
        "times": [
            "11:30 - 12:20",
            "14:30 - 15:20",
            "16:30 - 17:20",
        ],
    },
    "massage10": {
        "name": "Руки + шейно-воротниковая зона",
        "duration": "40 мин",
        "price": "800р",
        "times": [
            "10:45 - 11:25",
            "13:45 - 14:25",
            "15:45 - 16:25",
        ],
    },
    "massage11": {
        "name": "Спина + рефлекторно-сегментарный массаж",
        "duration": "60 мин",
        "price": "1500р",
        "times": [
            "9:15 - 10:15",
            "12:15 - 13:15",
            "14:45 - 15:45",
        ],
    },
    "massage12": {
        "name": "Спина + шейно-воротниковая зона + рефлекторно-сегментарный массаж",
        "duration": "80 мин",
        "price": "2000р",
        "times": [
            "11:45 - 13:05",
            "15:30 - 16:50",
        ],
    },
    "massage13": {
        "name": "Массаж лица",
        "duration": "60 мин",
        "price": "1300р",
        "times": [
            "12:00 - 13:00",
            "15:00 - 16:00",
        ],
    },
}

# Словарь с доступными часами для записи
available_hours = {
    9: "9:00 - 10:00",
    10: "10:00 - 11:00",
    11: "11:00 - 12:00",
    12: "12:00 - 13:00",
    13: "13:00 - 14:00",
    14: "14:00 - 15:00",
    15: "15:00 - 16:00",
    16: "16:00 - 17:00",
    17: "17:00 - 18:00",
}



logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Определение состояний анкеты
NAME, PHONE, COMPLAINTS, CHOOSING_MASSAGE, CHOOSING_TIME = range(5)

# Создание словаря для хранения данных анкеты
user_data = {}


# Функция для начала заполнения анкеты
async def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! Давайте начнем заполнение анкеты.\n"
        "Введите ваше имя и фамилию."
    )
    return NAME


# Функция для получения имени и фамилии
async def get_name(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    user_data['name'] = update.message.text
    await update.message.reply_text(
        "Отлично! Теперь введите ваш номер телефона."
    )
    return PHONE


# Функция для получения номера телефона
async def get_phone(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    user_data['phone'] = update.message.text
    await update.message.reply_text(
        "Спасибо! Напишите, пожалуйста, ваши жалобы или причины для массажа."
    )
    return COMPLAINTS


# Функция для завершения заполнения анкеты и вывода меню
async def done(update: Update, context: CallbackContext) -> int:
    user_data['complaints'] = update.message.text
    await update.message.reply_text(
        f"Спасибо, {user_data['name']}! Вы успешно заполнили анкету.\n"
        "Теперь вы можете выбрать действие:",
        reply_markup=main_menu()
    )
    return ConversationHandler.END


# Функция для вывода основного меню
def main_menu():
    keyboard = [['Информация', 'Прайс'], ['Анкета', 'Запись']]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)


# Функция для обработки команды /start
def start_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привет! Я бот для записи на массаж. Выберите действие:",
        reply_markup=main_menu()
    )


# Функция для обработки команды "Информация"
async def info(update: Update, context: CallbackContext):
    await update.message.reply_text(f"Информация о массажисте и адресе массажного салона.")
    await update.message.reply_photo(open('info.jpg', 'rb'))


# Функция для обработки команды "Прайс"
async def price(update: Update, context: CallbackContext):
    # Открываем и читаем фотографии
    with open('price_list1.jpg', 'rb') as photo1, open('price_list2.jpg', 'rb') as photo2:
        # Создаем список медиа-группы
        media = [
            InputMediaPhoto(media=photo1),
            InputMediaPhoto(media=photo2),
        ]

        # Отправляем медиа-группу
        await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media)


# Функция для обработки команды "Анкета"
async def questionnaire(update: Update, context: CallbackContext):
    user = update.message.from_user
    await update.message.reply_text(
        f"Ваша анкета:\n"
        f"Имя и фамилия: {user_data['name']}\n"
        f"Номер телефона: {user_data['phone']}\n"
        f"Жалобы и причины для массажа: {user_data['complaints']}\n"
        "Вы можете изменить анкету, нажав /start и начав заполнение заново."
    )


# Функция для обработки команды "Запись"
async def book(update: Update, context: CallbackContext):
    if 'name' not in user_data:
        await update.message.reply_text(
            "Прежде чем записаться на массаж, пожалуйста, заполните анкету."
        )
        return NAME

    # Создаем клавиатуру с вариантами массажа
    keyboard = [
        [InlineKeyboardButton("Общий массаж всего тела (70-80 мин) - 2000р", callback_data="massage1")],
        [InlineKeyboardButton("Релакс массаж (60 мин) - 1300р", callback_data="massage2")],
        [InlineKeyboardButton("Массаж спины (45 мин) - 1000р", callback_data="massage3")],
        [InlineKeyboardButton("Массаж шейно-воротниковой зоны (30 мин) - 500р", callback_data="massage4")],
        [InlineKeyboardButton("Массаж ног (30 мин) - 500р", callback_data="massage5")],
        [InlineKeyboardButton("Массаж рук (30 мин) - 300р", callback_data="massage6")],
        [InlineKeyboardButton("Массаж головы (20 мин) - 300р", callback_data="massage7")],
        [InlineKeyboardButton("Спина + ноги (60 мин) - 1500р", callback_data="massage8")],
        [InlineKeyboardButton("Спина + шейно-воротниковая зона (50 мин) - 1300р", callback_data="massage9")],
        [InlineKeyboardButton("Руки + шейно-воротниковая зона (40 мин) - 800р", callback_data="massage10")],
        [InlineKeyboardButton("Спина + рефлекторно-сегментарный массаж (60 мин) - 1500р", callback_data="massage11")],
        [InlineKeyboardButton("Спина + шейно-воротниковая зона + рефлекторно-сегментарный массаж (80 мин) - 2000р", callback_data="massage12")],
        [InlineKeyboardButton("Массаж лица (60 мин) - 1300р",
                              callback_data="massage13")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Выберите тип массажа:",
        reply_markup=reply_markup
    )

    # Переключаем состояние на выбор массажа
    return CHOOSING_MASSAGE


# Функция для обработки выбора типа массажа
async def choose_massage(update: Update, context: CallbackContext):
    query = update.callback_query
    user_data['selected_massage'] = query.data
    massage_info = massage_data.get(query.data)

    if massage_info:
        user_data['massage_name'] = massage_info["name"]
        user_data['massage_duration'] = massage_info["duration"]
        user_data['massage_price'] = massage_info["price"]

        keyboard = [
            [InlineKeyboardButton(f"{hour}:00 - {hour + 1}:00", callback_data=f"time{hour}")]
            for hour in available_hours
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            f"Вы выбрали: {user_data['massage_name']}\n"
            f"Длительность: {user_data['massage_duration']}\n"
            f"Цена: {user_data['massage_price']}\n"
            "Теперь выберите время для записи."
        )

        await query.message.reply_text(
            "Выберите желаемое время для записи:",
            reply_markup=reply_markup
        )

        # Переключаем состояние на выбор времени
        return CHOOSING_TIME
    else:
        await query.message.reply_text("Извините, что-то пошло не так. Пожалуйста, попробуйте ещё раз.")
        return ConversationHandler.END


# Функция для обработки выбора времени
async def choose_time(update: Update, context: CallbackContext):
    query = update.callback_query
    user_data['selected_time'] = query.data

    massage_name = user_data.get('massage_name', 'не указан')
    massage_duration = user_data.get('massage_duration', 'не указан')
    massage_price = user_data.get('massage_price', 'не указан')
    selected_time = user_data['selected_time']
    selected_hour = int(selected_time[4:])  # Извлекаем час из "timeX" (например, из "time9")

    bot = context.bot
    await bot.send_message(
        chat_id='1491596040',
        text=f"Имя и фамилия: {user_data['name']}\n" \
             f"Номер телефона: {user_data['phone']}\n" \
             f"Жалобы и причины для массажа: {user_data['complaints']}\n" \
             f"Выбранный тип массажа: {massage_name}\n" \
             f"Длительность: {massage_duration}\n" \
             f"Цена: {massage_price}\n" \
             f"Выбранное время: {selected_hour}:00 - {selected_hour + 1}:00"
    )

    message = f"Запись отправлена массажисту, скоро с вами свяжуться для уточнения записи!\n" \
              f"Имя и фамилия: {user_data['name']}\n" \
              f"Номер телефона: {user_data['phone']}\n" \
              f"Жалобы и причины для массажа: {user_data['complaints']}\n" \
              f"Выбранный тип массажа: {massage_name}\n" \
              f"Длительность: {massage_duration}\n" \
              f"Цена: {massage_price}\n" \
              f"Выбранное время: {selected_hour}:00 - {selected_hour + 1}:00"

    await query.message.reply_text(message)

    # Возвращаемся в основное состояние
    return ConversationHandler.END




def main():
    application = ApplicationBuilder().token('6489611390:AAG1rQWJc6jGsj1kG00kUsu23_k_x6D7aS0').build()

    # Создание обработчиков для команд и сообщений
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_name)],
            PHONE: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_phone)],
            COMPLAINTS: [MessageHandler(filters.TEXT & (~filters.COMMAND), done)],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.COMMAND | filters.Regex("^Информация$"), info))
    application.add_handler(MessageHandler(filters.COMMAND | filters.Regex("^Прайс"), price))
    application.add_handler(MessageHandler(filters.COMMAND | filters.Regex("^Запись"), book))
    application.add_handler(MessageHandler(filters.COMMAND | filters.Regex("^Анкета"), questionnaire))
    # Создание обработчика для выбора массажа
    choose_massage_handler = CallbackQueryHandler(choose_massage, pattern=r'^massage\d+$')

    # Создание обработчика для выбора времени
    choose_time_handler = CallbackQueryHandler(choose_time, pattern=r'^time\d+$')

    # Добавление обработчиков в диспетчер
    application.add_handler(choose_massage_handler, group=1)
    application.add_handler(choose_time_handler, group=1)

    # Запуск бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

