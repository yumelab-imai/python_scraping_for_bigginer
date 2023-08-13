import csv
import requests
from bs4 import BeautifulSoup

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

info_urls = set()  # 重複なくinfo_urlを保存するための集合
products = []

for div in product_divs:
    product = {}

    # 商品名
    name_link = div.find('h2', class_='title-link-wrapper--2sUFJ title-link-wrapper-grid--db8v2').find('a')
    # if name_link:
    #     product['name'] = name_link.text.strip()
    # else:
    #     product['name'] = None

    # 商品URL
    scraping_url = div.find('h2').find('a')
    if scraping_url:
        product['url'] = scraping_url.get('href')

        # 商品URLから商品詳細ページを取得
        product_response = requests.get(product['url'])
        product_soup = BeautifulSoup(product_response.content, "html.parser")

        # idがpagebodyであるdivタグを検索
        pagebody_div = product_soup.body.find('div', id='pagebody')

        # idがpagebodyであるdivタグを検索
        if pagebody_div:
            # 商品詳細ページの中の https://www.rakuten.co.jp/〇〇/info.html を抽出
            info_link = pagebody_div.find('a', href=lambda x: x and "info.html" in x)
            if info_link:
                info_url = info_link.get('href')
                if info_url not in info_urls:  # 重複していない場合のみ処理を実行
                    info_urls.add(info_url)  # 重複を防ぐため集合にURLを追加
                    print(f"info_url: {info_url}")  # info_urlを表示
                #     product['info_url'] = info_url

                    # product['info_url']から詳細ページを取得
                    # info_response = requests.get(product['info_url'])
                    # info_soup = BeautifulSoup(info_response.content, "html.parser")

                    # # 商品詳細ページの『<td valign="top">』の初めの部分を抽出
                    # td_valign_top = info_soup.find('td', {'valign': 'top'})
                    # if td_valign_top:
                    #     product['top_valign_content'] = td_valign_top.text.strip()
                    # else:
                    #     product['top_valign_content'] = None
                # else:
                #     product['info_url'] = None
                #     product['top_valign_content'] = None
            else:
                product['info_url'] = None
                product['top_valign_content'] = None
        else:
            product['info_url'] = None
            product['top_valign_content'] = None
    else:
        product['url'] = None

    products.append(product)

# 重複なく取得した会社情報のURLをprintで出力
for info_url in info_urls:
    print(info_url)

# CSVファイルへ書き込み
# keys = ['name', 'url', 'info_url', 'top_valign_content']
# with open('analysis_data/rakuten_products.csv', 'w', newline='', encoding='utf-8') as output_file:
#     dict_writer = csv.DictWriter(output_file, keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(products)