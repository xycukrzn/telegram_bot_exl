import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from collections import defaultdict

# Настройка журналирования
logging.basicConfig(level=logging.INFO)

# Создание бота и диспетчера
bot_token = '6342337990:AAHqxBkQUMFtDtQTl-OaWpWcrLlW33MLRK4'
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Словарь для подсчета голосов
votes = defaultdict(int)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Здорово, тигеры! Я чат-бот. Я открою кто из вас мразь:\n"
                        "/help - показать справку\n"
                        "/vote - голосуй за МРАЗЬ")

# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    response = "Вот список доступных команд:\n"
    response += "/help - показать справку\n"
    response += "/vote - начать голосование за главную мразь\n"
    response += "/results - показать результаты голосования"
    await message.answer(response)

# Обработчик команды /vote
@dp.message_handler(commands=['vote'])
async def vote_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    options = ["Дрон", "Бобер", "Звёздочка", "Хусейн-Великий", "Еврей-понторез"]
    for option in options:
        callback_data = f"vote_{option}"
        keyboard.add(types.InlineKeyboardButton(text=option, callback_data=callback_data))
    await message.answer("Выберите ту самую мразоту:", reply_markup=keyboard)

# Обработчик данных голосования
@dp.callback_query_handler(lambda c: c.data.startswith('vote_'))
async def process_vote(callback_query: types.CallbackQuery):
    option = callback_query.data.split('_')[1]
    votes[option] += 1
    await callback_query.answer(f"Вы проголосовали за {option}")

# Обработчик команды /results
@dp.message_handler(commands=['results'])
async def results_command(message: types.Message):
    response = "Результаты голосования:\n"
    total_votes = sum(votes.values())
    if total_votes > 0:
        for option, count in votes.items():
            percentage = (count / total_votes) * 100
            response += f"{option}: {count} голосов ({percentage:.2f}%)\n"
        max_votes = max(votes, key=votes.get)
        response += f"\nМразью является: {max_votes}"
    else:
        response += "Голосов пока нет"
    await message.answer(response)

# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
