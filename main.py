import csv
import requests
from bs4 import BeautifulSoup

URL = 'https://www.kivano.kg/noutbuki'
CSV = 'kivano_noutbuki.csv'
HOST = 'https://www.kivano.kg/'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'

}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params, verify=False)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_="item product_listbox oh")
    laptops = []
    for item in items:
        laptops.append({
            'Название': item.find('div', class_='listbox_title oh').get_text(),
            'Описание': str(item.find('div', class_='product_text pull-left').get_text()).split('\n')[-1],
            'Фото' :  'https://www.kivano.kg' + item.find('img').get('src'),
            'Цена' : item.find('div', class_='listbox_price text-center').get_text(),
            'Подробнее' : 'https://www.kivano.kg' + item.find('div', class_='listbox_title oh').find('a').get('href'),
            'Наличие' : item.find('div', class_='listbox_motive text-center').get_text()
        })
    return laptops

def save(items, path):
    with open(path, 'w') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Описание', 'Фото', 'Цена', 'Подробнее','Наличие'])
        for item in items:
            writer.writerow([item['Название'], item['Описание'], item['Фото'], item['Цена'], item['Подробнее'], item['Наличие']])

def parser():
    PAGENATION = int(input('Введите номер страницы: ').strip())
    html = get_html(URL)
    if html.status_code == 200:
        new_list = []
        for page in range(1, PAGENATION+1):
            print(f'Страница {page} готова')
            html = get_html(URL, params={'page' : page})
            new_list.extend(get_content(html.text))
        save(new_list, CSV)
        print('Завершено')
    else:
        print('Нет соединения')

if __name__ == '__main__':
    parser()