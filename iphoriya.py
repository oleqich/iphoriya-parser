from itertools import product
from bs4 import BeautifulSoup
from pprint import pprint
import requests
import csv

CSV = 'iphoriya.csv'
HOST = 'https://iphoriya.ru/'
URL = {
    'iphone': 'https://iphoriya.ru/product-category/iphone/',
    'ipad': 'https://iphoriya.ru/product-category/ipad/',
    'watch': 'https://iphoriya.ru/product-category/watch/',
    'mac': 'https://iphoriya.ru/product-category/mac/',
    'airpods': 'https://iphoriya.ru/product-category/airpods/'
}
DEVICES = {
            'iphone' : ['iphone-13-pro-max', 'iphone-13-pro', 'iphone-13', 'iphone-13-mini', 'iphone-se-2022', 'iphone-12-pro-max', 'iphone-12-pro', 'iphone-12', 'iphone-12-mini', 'iphone-12-mini', 'iphone-11', 'iphone-se-2020', 'iphone-xr'],
            'ipad' : ['ipad-pro-12-9-2021', 'ipad-pro-11-2021', 'ipad-air-2022', 'ipad-air-2020', 'ipad-2021', 'ipad-mini-2021']
}
#print(DEVICES)
        
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}

def get_html(url, params=''): 
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find('div', class_='row row_lg_3 row_md_2 row_sm_1 col_lg_3_4 col_md_1_1 col_sm_1_1').find_all('div')
    products = []
    for item in items:
        if 'card-product main-box' not in str(item):
            continue
        else:
            products.append(
                {
                'name' : item.find('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link').get('title'),
                'price' : item.find('div', class_='card-product-content').find('span', class_='woocommerce-Price-amount amount').text,
                'link' : item.find('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link').get('href')
                }
            )
    return products

def save_doc(items, path):
    with open(path, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['device', 'price', 'link'])
        for item in items:
            writer.writerow([item['name'], item['price'], item['link']])

def parser():
    products = []
    for device in DEVICES:
        for i in range(0, len(DEVICES[device])):
            html = get_html(URL[device]+DEVICES[device][i])
            if html.status_code == 200:
                products.extend(get_content(html.text))
                pass
            else:
                print('Error')
    save_doc(products, CSV)
    
    
parser()
