from aiogram import Bot, Dispatcher, executor, types
from client.znanija import Znanija
import os

bot = Bot(token="1644466038:AAH2C43ArCoNfTb2GQJa4MxHQ3EpeZ82G7E")
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Привет! Задай вопрос и получи ответ.")


@dp.message_handler()
async def answer_handler(message: types.Message):
    znanija = Znanija()
    try:
        answer = znanija.get_answers(message.text[8:], count=1)[0]
        if answer.attachment:
            file = znanija.get_attachment(answer)
            if file:
                await bot.send_photo(message.chat.id, photo=open(file, "rb"),
                                     caption=f"Ответ на вопрос <b>\"{answer.question}\"</b>:\n\n<em>{answer.answer}"
                                             f"</em>\n\n<a href=\"{answer.url}\">Вопрос на znanija.com</a>",
                                     parse_mode="html")
        else:
            await message.answer(f"Ответ на вопрос <b>\"{answer.question}\"</b>:\n\n<em>{answer.answer}</em>\n\n"
                                 f"<a href=\"{answer.url}\">Вопрос на znanija.com</a>", parse_mode="html",
                                 disable_web_page_preview=True)
    except IndexError:
        await message.answer("Не найдет ответ на ваш вопрос. Попробуйте изменить слова на синонимы.")


if __name__ == "__main__":
    for media in os.listdir("media"):
        os.remove(f"media/{media}")
    executor.start_polling(dp, skip_updates=True)
