print("Hello World!!!")


import csv
import requests
from bs4 import BeautifulSoup
import time

# 楽天のURL
url = "https://www.rakuten.co.jp/category/562084/?l2-id=shop_header_rgenre3"

# URLからWebページを取得
response = requests.get(url)

# BeautifulSoupオブジェクトを作成
soup = BeautifulSoup(response.content, "html.parser")

# <body>タグ内を取得
body = soup.body

# <body>タグ内の、dui-card searchresultitem クラスを含む div タグをすべて抽出
product_divs = body.find_all('div', class_='dui-card searchresultitem')

products = []
for div in product_divs:
    product = {}

    # 商品名
    name_link = div.find('h2', class_='title-link-wrapper--2sUFJ title-link-wrapper-grid--db8v2').find('a')
    if name_link:
        product['name'] = name_link.text.strip()
    else:
        product['name'] = None
    
    # 商品URL
    scraping_url = div.find('h2').find('a')
    if scraping_url:
        print('url')
        product['url'] = scraping_url.get('href')

        # 商品URLから商品詳細ページを取得(23 seconds)
        # time.sleep(0.5)  # 0.5秒待つ
        product_response = requests.get(product['url'])
        product_soup = BeautifulSoup(product_response.content, "html.parser")

        # idがpagebodyであるdivタグを検索
        pagebody_div = product_soup.body.find('div', id='pagebody')

        # idがpagebodyであるdivタグを検索
        if pagebody_div:
            # 商品詳細ページの中の https://www.rakuten.co.jp/〇〇/info.html を抽出
            info_link = pagebody_div.find('a', href=lambda x: x and "info.html" in x)
            if info_link:
                print('info_url')
                product['info_url'] = info_link.get('href')
                
                # product['info_url']から詳細ページを取得
                info_response = requests.get(product['info_url'])
                info_soup = BeautifulSoup(info_response.content, "html.parser")

                # 商品詳細ページの『<td valign="top">』の初めの部分を抽出
                td_valign_top = info_soup.find('td', {'valign': 'top'})
                print('top_valign_content')
                if td_valign_top:
                    print('top_valign_content')
                    product['top_valign_content'] = td_valign_top.text.strip()
                    print(f"top_valign_content: {product['top_valign_content']}")  # top_valign_content を表示
                else:
                    product['top_valign_content'] = None
                print(f"top_valign_content: {product['top_valign_content']}")  # top_valign_content を表示
            else:
                product['info_url'] = None
                product['top_valign_content'] = None
        else:
            product['info_url'] = None
            product['top_valign_content'] = None
    else:
        product['url'] = None

    products.append(product)
    print(f"info_url: {product['info_url']}")  # info_urlを表示
    # break  # ループを一回で終了


# CSVファイルへ書き込み
# keys = ['url', 'info_url', 'top_valign_content']
keys = ['name', 'url', 'info_url']
with open('analysis_data/rakuten_products.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(products)