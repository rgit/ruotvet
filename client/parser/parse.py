from bs4 import BeautifulSoup
from requests import Response
import re


class Parser:
    @staticmethod
    def _regex_find(text: str):
        return re.findall(r"(<span>(.+?)</span>)", text)[0][1]

    def parse_search_results(self, response: Response):
        soup = BeautifulSoup(response.text, "html.parser")
        output = []
        for iteration in soup.find_all(href=True):
            if iteration:
                h3_element = iteration.findChildren("h3")
                if h3_element:
                    output.append([self._regex_find(str(h3_element[0])), iteration["href"]])
        return output

    @staticmethod
    def _contains_stop_word(word: str):
        stop_words = ["реклам", "отключ", "доступ", "отве", "вход", "выход", "регистра", "войти", "выйти",
                      "зарегистриров"]
        for stop_word in stop_words:
            if stop_word in word:
                return True
        return False

    def prepare_text(self, text: list):
        output = []
        for word in text:
            if not self._contains_stop_word(word):
                if word not in output:
                    output.append(word)
        return output
