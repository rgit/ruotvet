from client.google import Google

g = Google()

# https://znanija.com/app/ask?entry=top&q=ТУТВОПРОС

print(
    # g.search_for_page("https://znanija.com/task/29242596").text
    g.search_for_links("Площадь прямоугольного треугольника равна 6, а длина медианы".split())
)


