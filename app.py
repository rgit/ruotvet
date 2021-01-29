from ruotvet.otvetmail import OtvetMail
from ruotvet.znanija import Znanija

zn = Znanija()
otvet = OtvetMail()


question = "гомологу этиленгликоля соотвецтвует формула"

print(
    zn.get_answers(question, count=1), "Znanija.com"
)

print(
    otvet.get_answers(question, count=1), "otvet.mail.ru"
)
