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

from ruotvet.otvetmail import OtvetMail
from ruotvet.znanija import Znanija
from ruotvet.yandexq import YandexQ


question = "Линейная функция задана формулой: y=−x+14 Найдите значение аргумента, при котором значение функции равно: 9.?"


print(OtvetMail.get_answers(query=question, count=1), "Znanija.com")
print(Znanija().get_answers(query=question, count=1), "otvet.mail.ru")
print(YandexQ().get_answers(query=question, count=1), "q.yandex.ru")
