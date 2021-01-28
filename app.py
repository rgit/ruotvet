from client.otvetmail import OtvetMail
from client.znanija import Znanija

zn = Znanija()
otvet = OtvetMail()


question = "гомологу этиленгликоля соотвецтвует формула"

print(
    zn.get_answers(question, count=1), "Znanija.com"
)

print(
    otvet.get_answers(question, count=1), "otvet.mail.ru"
)
