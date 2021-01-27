from aiogram import Bot, Dispatcher, executor, types
from client.znanija import Znanija

bot = Bot(token="1644466038:AAH2C43ArCoNfTb2GQJa4MxHQ3EpeZ82G7E")
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Привет! Задай вопрос с помощью команды /answer {вопрос тут}.")


@dp.message_handler(commands="answer")
async def answer_handler(message: types.Message):
    try:
        if message.text[8:]:
            znanija = Znanija()
            answer = znanija.get_answers(message.text[8:], count=0)[0]
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
        else:
            await message.answer("Задайте вопрос с помощью команды /answer {вопрос тут}.")
    except IndexError:
        await message.answer("Задайте вопрос с помощью команды /answer {вопрос тут}.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
