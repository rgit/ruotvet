from ruotvet.otvetmail import OtvetMail
from ruotvet.znanija import Znanija

# from ruotvet.utils import Recognizer
#
# zn = Znanija()
# otvet = OtvetMail()
#
#
# question = " ".join(Recognizer().get_text_from_image("ruotvet/utils/img.png").split()[:8])
#
# print(question)

# question = ""
#
# print(
#     zn.get_answers(question, count=1), "Znanija.com"
# )
#
# print(
#     otvet.get_answers(question, count=1), "otvet.mail.ru"
# )


from ruotvet.yandexq import YandexQ

print(
    YandexQ().get_answers("Что реагирует с раствором гидроксида калия?", count=1)
)
