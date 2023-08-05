print("Hello World!!!")


import csv
import requests
from bs4 import BeautifulSoup


# AmazonのURL
url = "https://www.amazon.co.jp/s?k=%E9%9F%93%E5%9B%BD%E3%82%B3%E3%82%B9%E3%83%A1&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=2HGHTZJ98Z987&sprefix=%E9%9F%93%E5%9B%BD%E3%82%B3%E3%82%B9%E3%83%A1%2Caps%2C194&ref=nb_sb_noss_1"

# URLからWebページを取得
response = requests.get(url)

# BeautifulSoupオブジェクトを作成
soup = BeautifulSoup(response.content, "html.parser")

# <body>タグ内を取得
body = soup.find('body')

# <body>タグ内の、a-section と a-spacing-base のクラスを持つ div タグをすべて抽出
product_divs = body.find_all('div', class_='a-section a-spacing-base')

products = []
for div in product_divs:
    product = {}
    
    # 商品名
    name_span = div.find('span', class_='a-size-base-plus a-color-base a-text-normal')
    if name_span:
        # text.strip()とは？
        product['name'] = name_span.text.strip()
    else:
        product['name'] = None
    
    # 星の数
    rating_span = div.find('span', {'aria-label': True})
    if rating_span:
        product['rating'] = rating_span.get('aria-label').strip()
    else:
        product['rating'] = None

    # 価格
    price_span = div.find('span', class_='a-price-whole')
    if price_span:
        product['price'] = price_span.text.strip() + "円"
    else:
        product['price'] = None

    # 商品詳細URL
    scraping_url = div.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
    if scraping_url:
        product['url'] = "https://www.amazon.co.jp/" + scraping_url.get('href')
    else:
        product['url'] = None

    products.append(product)

# CSVファイルへ書き込み
keys = ['name', 'rating', 'price', 'url']
with open('analysis_data/products.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(products)
