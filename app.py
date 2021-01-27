from client.google import Google

g = Google()

query = "Формулы косинуса суммы"

# answers = g.search_for_links(query.split())
#
# for answer in answers:
#     print(answer + "\n")

print(
    g.search(query).text
)


# # A private "znanija.com" api here -> ru-api.z-dn.net
