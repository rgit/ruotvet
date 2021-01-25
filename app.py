from client.google import Google

g = Google()

# for r in g.search(input("Введите запрос: ").split()):
#     print(f"По запросу найдена страница {r[0]}. Ссылка: {r[1]}")


# https://znanija.com/app/ask?entry=top&q=ТУТВОПРОС

print(
    g.search_for_page("https://znanija.com/task/29242596").text
)


