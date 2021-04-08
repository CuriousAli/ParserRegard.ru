import requests
from bs4 import BeautifulSoup
import csv

# Constants
CSV = 'videocards.csv'
HOST = 'https://www.regard.ru'
URL = 'https://www.regard.ru/catalog/group4037/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
}

# Get status code. Expected 200
def get_html(url, params =''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

# Parse logic, searching and recive required parameters.
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='block')
    videocards = []

    for item in items:
        videocards.append(
            {
                'title': item.find('div', class_='aheader').find('a', class_='header').get_text(strip=True),
                'link_product': HOST + item.find('div', class_='aheader').find('a').get('href'),
                'price': item.find('div', class_='price').get_text(strip=True),
                'VCard_img': HOST + item.find('div', class_='block_img').find('img').get('src')
            }
        )
    return videocards

#Save recived data into SCV file
def save_result(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Ссылка на продукт','Цена', 'Изображение видеокарты'])
        for item in items:
            writer.writerow([item['title'], item['link_product'], item['price'], item['VCard_img']])

# General function
def parser():
    PAGINATION = input('Укажите количество страниц для парсинга: ')
    PAGINATION = int(PAGINATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        videocards = []
        for page in range(1, PAGINATION):
            print(f'Происходит парсинг страницу №  {page}')
            html = get_html(URL, params={'page': page})
            videocards.extend(get_content(html.text))
            save_result(videocards, CSV)
        pass
    else:
        print('Error')

parser()