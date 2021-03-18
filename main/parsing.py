import requests
from bs4 import BeautifulSoup

import threading


def get_html(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
    response = requests.get(url, headers=headers)
    return response.text


def get_page_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    product_list = soup.find('div', class_="col-article content")
    products = product_list.find_all('div', class_="media-body")
    list_ = []
    for product in products:
        # photo = product.find('div', class_="media").find('div',class_='img').get('src')
        title = product.find('div', class_="item-title").find('a').text
        title = title.strip()
        description = product.find('p').text

        data = {'title': title, 'description': description}
        list_.append(data)
    return list_

def main():
    nootebooks_url = 'https://мтв.онлайн/feed/tags/%D0%B3%D1%80%D0%B8%D0%B1%D1%8B'
    pages = '/'

    total_pages = get_html(nootebooks_url)
    # print(total_pages)

    for page in range(3):  # 37
        url_with_page = nootebooks_url + pages + str(page)
        html = get_html(url_with_page)
        _list_ = get_page_data(html)
    return _list_



