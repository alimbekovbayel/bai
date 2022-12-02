# import requests
# from bs4 import BeautifulSoup
# import json
# URl = "https://news.ycombinator.com/  "
HEADERS = {
     'user-agent': 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
     }
import requests
from pprint import pprint
from bs4 import BeautifulSoup
import json



URL = 'https://news.ycombinator.com/'
def get_html(url):
    r = requests.get(url)
    return r.content

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('tr', class_='athing')
    new_list = []
    for item in items:
        new_list.append({
            'Title' : item.find('span', class_='titleline').get_text(),
            'Title Link' : item.find('span', class_='titleline').find('a').get('href'),
            'Point': (soup.find ('span',class_='score').get_text()),
            'HOUR':(soup.find('span',class_='age').get_text()),
            'COMENTS':str(soup.find('span',class_='subline').get_text().split()[-2]),
            'COMENTS LINK':'https://news.ycombinator.com/' + soup.find('span',class_='age').find('a').get('href'),
        })
    return new_list

def save(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)
        pprint(data)
save(get_content(get_html(URL)))



