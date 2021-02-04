from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.handler import SkipHandler, CancelHandler
from aiogram import Bot, Dispatcher, executor, types
from ruotvet import Znanija, YandexQ, OtvetMail, SuperResheba
from ruotvet.utils import Database
import os

bot = Bot(token="1644466038:AAH2C43ArCoNfTb2GQJa4MxHQ3EpeZ82G7E", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    if not Database().select(table="users", user_id=str(message.from_user.id)):
        Database().insert(table="users", user_id=str(message.from_user.id))
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup_columns = (("Яндекс Q", "yandexq"), ("Знания", "znanija"), ("Ответы майл.ру", "otvetmail"))
        markup_buttons = (types.InlineKeyboardButton(text, callback_data=data) for text, data in markup_columns)
        markup.row(*markup_buttons)
        markup.add(
            types.InlineKeyboardButton("Связаться с создателем", url="https://fesh.us/"),
        )
        msg = await message.answer("Привет! Выбери где будем искать по-умолчанию <em>(Можно будет изменить)</em>:",
                                   reply_markup=markup)
        await dp.storage.set_data(chat=message.chat.id, user=message.from_user.id, data={"message": msg})
    else:
        await message.answer("Здравствуйте. Напишите вопрос, или скиньте фото, где он четко виден.")


@dp.message_handler(commands="settings")
async def settings_handlers(message: types.Message):
    current_client = Database().select(table="users", user_id=str(message.from_user.id))[0].default_client
    if current_client == 1:
        current_client = "Знания.ком"
    elif current_client == 2:
        current_client = "Яндекс Q"
    elif current_client == 3:
        current_client = "Ответы Майл.ру"
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup_columns = (("Яндекс Q", "yandexq"), ("Знания", "znanija"), ("Ответы майл.ру", "otvetmail"))
    markup_buttons = (types.InlineKeyboardButton(text, callback_data=data) for text, data in markup_columns)
    markup.row(*markup_buttons)
    markup.add(
        types.InlineKeyboardButton("Связаться с создателем", url="https://fesh.us/"),
    )
    msg = await message.answer(f"В настоящее время поиск производится в базе {current_client}. Для изменения нажмите "
                               f"на одну из кнопок ниже.", reply_markup=markup)
    await dp.storage.set_data(chat=message.chat.id, user=message.from_user.id, data={"message": msg})


@dp.callback_query_handler(text=["yandexq", "znanija", "otvetmail"])
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    msg = await dp.storage.get_data(chat=query.message.chat.id, user=query.from_user.id)
    msg = msg["message"]
    if query.data == "yandexq":
        await bot.edit_message_text("С этого момента поиск будет происходить в ответах Яндекс Q.", msg.chat.id,
                                    msg.message_id)
        Database().update("default_client", 2, table="users", user_id=str(query.from_user.id))
    elif query.data == "znanija":
        await bot.edit_message_text("С этого момента поиск будет происходить в ответах Знания.ком.", msg.chat.id,
                                    msg.message_id)
        Database().update("default_client", 1, table="users", user_id=str(query.from_user.id))
    elif query.data == "otvetmail":
        await bot.edit_message_text("С этого момента поиск будет происходить в ответах Майл.ру.", msg.chat.id,
                                    msg.message_id)
        Database().update("default_client", 3, table="users", user_id=str(query.from_user.id))
    raise CancelHandler


@dp.message_handler(commands="all")
async def all_query_handler(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    try:
        query = message.text.split("all ")[1]
    except IndexError:
        await message.answer("После команды должен идти вопрос. Пример – /all Корень отрицательного числа.")
        raise CancelHandler
    znanija_query = Znanija.get_answers(query=query, count=1)
    yandexq_query = YandexQ.get_answers(query=query, count=1)
    otvetmail_query = OtvetMail.get_answers(query=query, count=1)
    if znanija_query or yandexq_query or otvetmail_query:
        await message.answer(f"Ответ на вопрос <b>\"{message.text.split('all ')[1]}\"</b> от всех поисковых систем")
        if znanija_query:
            await message.answer(f"<b>Знания.ком:</b>\n\n<em>{znanija_query[0].answer}</em>\n\n<a "
                                 f"href='{znanija_query[0].url}'>Открыть в браузере</a>",
                                 disable_web_page_preview=True)
        if yandexq_query:
            await message.answer(f"<b>Яндекс Q:</b>\n\n<em>{yandexq_query[0].answer}</em>\n\n<a "
                                 f"href='{yandexq_query[0].url}'>Открыть в браузере</a>",
                                 disable_web_page_preview=True)
        if otvetmail_query:
            await message.answer(f"<b>Ответы майл.ру:</b>\n\n<em>{otvetmail_query[0].answer}</em>\n\n<a "
                                 f"href='{otvetmail_query[0].url}'>Открыть в браузере</a>",
                                 disable_web_page_preview=True)
    else:
        await message.answer("Не удалось найти ответы на ваш вопрос. Проверьте правильность написания вопроса или "
                             "попробуйте перефразировать.")
    raise CancelHandler


@dp.message_handler(commands="resheba")
async def resheba_query_handler(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    try:
        query = message.text.split("resheba ")[1]
    except IndexError:
        await message.answer("После команды должен идти вопрос. Пример – /resheba Математика 11 класс.")
        raise CancelHandler
    response = SuperResheba().get_answers(query=query, count=1)
    if response[0].attachments:
        await bot.send_media_group(message.chat.id, media=[types.InputMediaPhoto(open(attch, "rb"))
                                                           for attch in response[0].attachments])
        await message.answer(f"<b>Ответ на вопрос выше.</b>\n\n<a href='{response[0].url}'>Открыть в браузере</a>")
    else:
        await message.answer("Не удалось найти ответы на ваш вопрос. Проверьте правильность написания вопроса или "
                             "попробуйте перефразировать.")
    raise CancelHandler


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def default_client_query_handler(message: types.Message):
    default_client, answer = Database().select(table="users", user_id=str(message.chat.id))[0].default_client, []
    await bot.send_chat_action(message.chat.id, "typing")
    if default_client == 1:
        answer = Znanija.get_answers(query=message.text, count=1)
    elif default_client == 2:
        answer = YandexQ.get_answers(query=message.text, count=1)
    elif default_client == 3:
        answer = OtvetMail.get_answers(query=message.text, count=1)
    if answer:
        await message.answer(f"Ответ на вопрос <b>\"{message.text}\"</b>:\n\n<em>{answer[0].answer}</em>\n\n<a "
                             f"href='{answer[0].url}'>Открыть в браузере</a>", disable_web_page_preview=True)
    else:
        await message.answer("Не удалось найти ответ на ваш вопрос. Проверьте правильность написания вопроса или "
                             "попробуйте перефразировать.")
    raise CancelHandler



if __name__ == "__main__":
    for media in os.listdir("media"):
        os.remove(f"media/{media}")
    executor.start_polling(dp, skip_updates=True)
