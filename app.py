from ruotvet.otvetmail import OtvetMail
from ruotvet.znanija import Znanija

from ruotvet.utils import Recognizer

zn = Znanija()
otvet = OtvetMail()


question = " ".join(Recognizer().get_text_from_image("ruotvet/utils/img.png", threshold=True).split()[:8])

print(question)

print(
    zn.get_answers(question, count=3), "Znanija.com"
)
#
print(
    otvet.get_answers(question, count=3), "otvet.mail.ru"
)
