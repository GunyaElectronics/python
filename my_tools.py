import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re


def get_internal_links(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        internal_links = []
        for link in links:
            absolute_url = urljoin(url, link['href'])

            if urlparse(absolute_url).netloc == urlparse(url).netloc:
                internal_links.append(absolute_url)

        print("Посилання на сторінки того ж сайту:")
        for internal_link in internal_links:
            print(internal_link)
        return internal_links
    else:
        print("Не вдалося отримати доступ до сторінки.")
        return None


def main():
    with open("D:\\Gorenje.txt", 'r', errors='replace') as file:
        # Читання вмісту файлу
        text = file.read()
        text = text.lower()
        text = re.sub(r'[^a-zA-Z]', ' ', text)

    # Розділення тексту на слова
    words = text.split()

    # Використання множини для отримання унікальних слів
    unique_words = set(words)
    filtered_words = [word for word in unique_words if len(word) >= 3]
    # Виведення унікальних слів

    filtered_words.sort(key=len)
    filtered_words.sort()
    print("Унікальні слова:")
    for word in filtered_words:
        print(word)

    line = input()

    url = 'http://www.proradio.org.ua/netradio/index.php'

    links = get_internal_links(url)

    for link in links:
        response_inner = requests.get(link)

        if response_inner.status_code == 200:
            if '.m3u' in response_inner.text:
                for line in response_inner.text.split('\n'):
                    if '.m3u' in line:
                        soup = BeautifulSoup(line, 'html.parser')
                        m3u_links = soup.find_all('a', href=True)
                        for m3u_link in m3u_links:
                            absolute_url = urljoin(url, m3u_link['href'])
                            print(f"Посилання на M3U-файл: {absolute_url}")
        else:
            print(f"Не вдалося отримати вміст сторінки за посиланням: {link}")


if __name__ == '__main__':
    main()
