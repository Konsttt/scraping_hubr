import bs4
import requests
import re

URL = 'https://habr.com'

# Для обхода защиты на запросы не из браузера используем HEADERS браузера.
# Как получить requests headers:
# 1. Открываем сайт, в принципе можно любой. F12 - Networks.
# 2. На самом большом по времени запросе правой кнопкой и выбрать Copy as cURL bash
# 3. На сайте https://curlconverter.com/ вставить в окно вместо "curl exapmple.com" скопированный headers
# 4. Ниже получаем готовую обёртку headers и cookies для Python. Вставляем в свой код.
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru,en;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': '_ym_uid=1653904033856026553; _ym_d=1653904033; _ga=GA1.2.173305947.1653904033; _ym_isad=2; _gid=GA1.2.1060535166.1664723219',
    'If-None-Match': 'W/"6a3-52x/aBn+vaqSpcuwqXdFjHnBTNE"',
    'Referer': 'https://habr.com/ru/all/',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-site',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.114 YaBrowser/22.9.1.1094 Yowser/2.5 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Yandex";v="22"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

# KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'java', 'технология', 'кирпич']
pattern0 = r"^[Д,д](изайн)[^А-Яа-я1-9]|[^А-Яа-я1-9][Д,д](изайн)[^А-Яа-я1-9]"
pattern1 = r"^[Ф,ф](ото)[^А-Яа-я1-9]|[^А-Яа-я1-9][Ф,ф](ото)[^А-Яа-я1-9]"
pattern2 = r"^[P,p](ython)[^a-rt-wA-RT-W1-9]|[^a-wA-W1-9][P,p](ython)[^a-rt-wA-RT-W1-9]"
pattern3 = r"^[W,w](eb)[^a-wA-W1-9]|[^a-wA-W1-9][W,w](eb)[^a-wA-W1-9]"
pattern4 = r"^[J,j](ava)[^a-wA-W1-9]|[^a-wA-W1-9][J,j](ava)[^a-wA-W1-9]"
pattern5 = r"^[Т,т](ехнолог)([а-я]{1,4})?[^А-Яа-я1-9]|[^А-Яа-я1-9][Т,т](ехнолог)([а-я]{1,4})?[^А-Яа-я1-9]"
pattern6 = r"^[К,к](ирпич)([а-я]{1,4})?[^А-Яа-я1-9]|[^А-Яа-я1-9][К,к](ирпич)([а-я]{1,4})?[^А-Яа-я1-9]"
pattern7 = r"^[К,к](осм)([а-я]{1,7})?[^А-Яа-я1-9]|[^А-Яа-я1-9][К,к](осм)([а-я]{1,7})?[^А-Яа-я1-9]"
pattern8 = r"^[С,с](плав)([а-я]{1,3})?[^А-Яа-я1-9]|[^А-Яа-я1-9][С,с](плав)([а-я]{1,3})?[^А-Яа-я1-9]"

# patterns_dict = {'дизайн': pattern0, 'фото': pattern1, 'python': pattern2, 'web': pattern3, 'java': pattern4,
#                  'технология': pattern5, 'кирпич': pattern6, 'космос': pattern7, 'сплав': pattern8}
patterns_dict = {'дизайн': pattern0, 'фото': pattern1, 'python': pattern2, 'web': pattern3, 'java': pattern4}


# Функция поиска слова в тексте с помощью регулярного выражения
def search_word(pattern_dict, text_):
    for word_, pattern in pattern_dict.items():
        if re.search(pattern, text_):
            return word_  # Перед результатом дополнительно выводить слово, которое нашлось в данной статье
    return False


if __name__ == '__main__':
    response = requests.get(URL, headers=HEADERS)
    text = response.text  # html разметка старницы в виде одной строки.
    soup = bs4.BeautifulSoup(text, features='html.parser')  # Объект для скрапинга.
    articles = soup.find_all('article')
    for article in articles:

        # Вспомогательная функция для печати результата в случае, если слово нашлось. Чтобы не было дубликатов кода.
        def print_result():
            date_time = article.find(class_='tm-article-snippet__datetime-published').find('time').attrs['title']
            href_ = article.find(class_='tm-article-snippet__title-link').attrs['href']
            result = f'{date_time} - {title} - {URL}{href_}'  # <дата> - <заголовок> - <ссылка>
            print(word)  # Дополнительно перед результатом вывожу слово, по которому был поиск и оно есть в статье
            print(result)  # Печать результата
            print()

        # Сначала проверяем все паттерны в тексте заголовка статьи: если истина, то печатаем дата - заголовок - ссылка
        title = article.find('h2').find('span').text
        word = search_word(patterns_dict, title)
        if word:
            print_result()
            continue  # Если совпадение найдено, то внутри уже искать не нужно - переходим к следующей статье.

        # Теперь проверяем совпадение в тегах (если в заголовке не нашли)
        hubs = article.find_all(class_='tm-article-snippet__hubs-item-link')
        hubs_list = [hub.text.strip() for hub in hubs]
        hubs_list_text = ' '.join(hubs_list)
        word = search_word(patterns_dict, hubs_list_text)
        if word:
            print_result()
            continue

        # Теперь проверяем совпадение в тексте preview (если не нашли в заголовке и в тегах)
        preview_text = article.find(class_='tm-article-body tm-article-snippet__lead').text
        word = search_word(patterns_dict, preview_text)
        if word:
            print_result()
            continue

        # Если нет совпадений ни в одном из предыдущих блоков, то ищем во всей статье.
        # Ссылка на заголовок статьи и на "Читать далее" одинаковы, поэтому используем её
        href = article.find(class_='tm-article-snippet__title-link').attrs['href']
        url_full_article = URL + href
        response = requests.get(url_full_article, headers=HEADERS)
        text = response.text  # Получаем html ответ полного текста статьи
        soup2 = bs4.BeautifulSoup(text, features='html.parser')
        full_text = soup2.find(id='post-content-body').text  # Полный текст статьи без html тегов
        word = search_word(patterns_dict, full_text)  # Поиск паттернов по всему тексту статьи
        if word:
            print_result()
            print()





