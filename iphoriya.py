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
        writer.writerow(['phone', 'price', 'link'])
        for item in items:
            writer.writerow([item['name'], item['price'], item['link']])

def parser():
    html = get_html(URL['iphone']+'iphone-13-pro-max')
    if html.status_code == 200:
        products = []
        html = get_html(URL['iphone']+'iphone-13-pro-max')
        products.extend(get_content(html.text))
        save_doc(products, CSV)
        pass
    else:
        print('Error')
    
    
parser()
